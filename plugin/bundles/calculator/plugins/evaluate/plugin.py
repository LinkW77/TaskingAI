from bundle_dependency import *
import sympy as sp
from typing import Dict


class Evaluate(PluginHandler):
    async def execute(
        self, credentials: BundleCredentials, execution_config: Dict, plugin_input: PluginInput
    ) -> PluginOutput:
        expression: str = plugin_input.input_params.get("expression")
        try:
            expression = sp.sympify(expression)
            result = expression.evalf()
            return PluginOutput(data={"result": str(result)})
        except Exception as e:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid expression. Please provide a valid expression."
            )
