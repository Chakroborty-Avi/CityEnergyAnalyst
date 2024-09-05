from collections import defaultdict
from itertools import groupby
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import cea.config
import cea.scripts
from cea.schemas import schemas
from .utils import deconstruct_parameters
from cea.interfaces.dashboard.dependencies import CEAConfig

router = APIRouter()


class ToolDescription(BaseModel):
    name: str
    label: str
    description: str


class ToolProperties(ToolDescription):
    category: str
    categorical_parameters: Dict[str, List[Dict]]
    parameters: List[Dict]


@router.get('/')
async def get_tool_list(config: CEAConfig) -> Dict[str, List[ToolDescription]]:
    tools = cea.scripts.for_interface('dashboard', plugins=config.plugins)
    result = dict()
    for category, group in groupby(tools, lambda t: t.category):
        result[category] = [
            ToolDescription(name=t.name, label=t.label, description=t.description) for t in group
        ]
    return result


@router.get('/{tool_name}')
async def get_tool_properties(config: CEAConfig, tool_name: str) -> ToolProperties:
    script = cea.scripts.by_name(tool_name, plugins=config.plugins)

    parameters = []
    categories = defaultdict(list)
    for _, parameter in config.matching_parameters(script.parameters):
        parameter_dict = deconstruct_parameters(parameter, config)

        if parameter.category:
            categories[parameter.category].append(parameter_dict)
        else:
            parameters.append(parameter_dict)

    out = ToolProperties(
        name=tool_name,
        label=script.label,
        description=script.description,
        category=script.category,
        categorical_parameters=categories,
        parameters=parameters,
    )

    return out


@router.post('/{tool_name}/default')
async def restore_default_config(config: CEAConfig, tool_name: str):
    """Restore the default configuration values for the CEA"""
    default_config = cea.config.Configuration(config_file=cea.config.DEFAULT_CONFIG)

    for parameter in parameters_for_script(tool_name, config):
        if parameter.name != 'scenario':
            parameter.set(
                default_config.sections[parameter.section.name].parameters[parameter.name].get())
    await config.save()
    return 'Success'


@router.post('/{tool_name}/save-config')
async def save_tool_config(config: CEAConfig, tool_name: str, payload: Dict[str, Any]):
    """Save the configuration for this tool to the configuration file"""
    for parameter in parameters_for_script(tool_name, config):
        if parameter.name != 'scenario' and parameter.name in payload:
            value = payload[parameter.name]
            print('%s: %s' % (parameter.name, value))
            parameter.set(value)
    await config.save()
    return 'Success'


@router.get('/{tool_name}/check')
async def check_tool_inputs(config: CEAConfig, tool_name: str):
    script = cea.scripts.by_name(tool_name, plugins=config.plugins)
    schema_data = schemas(config.plugins)

    script_suggestions = set()

    for method_name, path in script.missing_input_files(config):
        _script_suggestions = schema_data[method_name]['created_by'] if 'created_by' in schema_data[method_name] else None

        if _script_suggestions is not None:
            script_suggestions.update(_script_suggestions)

    if script_suggestions:
        scripts = []
        for script_suggestion in script_suggestions:
            _script = cea.scripts.by_name(script_suggestion, plugins=config.plugins)
            scripts.append({"label": _script.label, "name": _script.name})

        raise HTTPException(status_code=400,
                            detail={"message": "Missing input files",
                                    "script_suggestions": list(scripts)})


def parameters_for_script(script_name, config):
    """Return a list consisting of :py:class:`cea.config.Parameter` objects for each parameter of a script"""
    parameters = [p for _, p in config.matching_parameters(
        cea.scripts.by_name(script_name, plugins=config.plugins).parameters)]
    return parameters
