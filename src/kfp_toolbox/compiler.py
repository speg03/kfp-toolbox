import importlib
from typing import Any, Callable, Mapping, Optional


def _pipeline_function_object(
    module: str,
    function_name: Optional[str] = None,
) -> Callable[..., Any]:
    from kfp.v2.compiler.main import PipelineCollectorContext

    if function_name:
        obj = importlib.import_module(module)
        try:
            obj = getattr(obj, function_name)
        except AttributeError:
            raise ValueError(f"'{module}' module has no function '{function_name}'.")
        function_obj = obj
    else:
        with PipelineCollectorContext() as pipeline_funcs:
            importlib.import_module(module)
        if len(pipeline_funcs) == 0:
            raise ValueError(
                f"There are no pipeline functions in the '{module}' module."
                f" Otherwise, have you already imported '{module}'?"
            )
        elif len(pipeline_funcs) > 1:
            raise ValueError(
                f"The '{module}' module has several pipeline functions."
                " You must specify the function_name."
            )
        function_obj = pipeline_funcs[0]

    return function_obj  # type: ignore


def _compile_pipeline_function_v1(
    package_path: str,
    legacy_mode: str,
    pyfile: Optional[str] = None,
    module: Optional[str] = None,
    function_name: Optional[str] = None,
    type_check: bool = True,
) -> None:
    from kfp.compiler import Compiler
    from kfp.compiler.main import compile_pyfile
    from kfp.dsl import PipelineExecutionMode

    execution_mode = PipelineExecutionMode.V1_LEGACY
    if legacy_mode == "V1_LEGACY":
        pass  # do nothing
    elif legacy_mode == "V2_COMPATIBLE":
        execution_mode = PipelineExecutionMode.V2_COMPATIBLE
    elif legacy_mode == "V2_ENGINE":
        execution_mode = PipelineExecutionMode.V2_ENGINE
    else:
        raise ValueError(
            "legacy_mode must be one of 'V1_LEGACY', 'V2_COMPATIBLE', or 'V2_ENGINE'."
        )

    if pyfile:
        compile_pyfile(
            pyfile=pyfile,
            function_name=function_name,
            output_path=package_path,
            type_check=type_check,
            mode=execution_mode,
        )
    elif module:
        pipeline_function = _pipeline_function_object(module, function_name)
        Compiler(mode=execution_mode).compile(
            pipeline_func=pipeline_function,
            package_path=package_path,
            type_check=type_check,
        )
    else:
        raise ValueError("You must specify either pyfile or module.")


def _compile_pipeline_function_v2(
    package_path: str,
    pyfile: Optional[str] = None,
    module: Optional[str] = None,
    function_name: Optional[str] = None,
    pipeline_parameters: Optional[Mapping[str, Any]] = None,
    type_check: bool = True,
) -> None:
    from kfp.v2.compiler import Compiler
    from kfp.v2.compiler.main import compile_pyfile

    if pyfile:
        compile_pyfile(
            pyfile=pyfile,
            function_name=function_name,
            pipeline_parameters=pipeline_parameters,
            package_path=package_path,
            type_check=type_check,
            use_experimental=False,
        )
    elif module:
        pipeline_function = _pipeline_function_object(module, function_name)
        Compiler().compile(
            pipeline_func=pipeline_function,
            package_path=package_path,
            pipeline_parameters=pipeline_parameters,
            type_check=type_check,
        )
    else:
        raise ValueError("You must specify either pyfile or module.")


def compile_pipeline_function(
    package_path: str,
    pyfile: Optional[str] = None,
    module: Optional[str] = None,
    function_name: Optional[str] = None,
    pipeline_parameters: Optional[Mapping[str, Any]] = None,
    type_check: bool = True,
    legacy_mode: Optional[str] = None,
) -> None:
    if legacy_mode:
        _compile_pipeline_function_v1(
            package_path=package_path,
            legacy_mode=legacy_mode,
            pyfile=pyfile,
            module=module,
            function_name=function_name,
            type_check=type_check,
        )
    else:
        _compile_pipeline_function_v2(
            package_path=package_path,
            pyfile=pyfile,
            module=module,
            function_name=function_name,
            pipeline_parameters=pipeline_parameters,
            type_check=type_check,
        )
