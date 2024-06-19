import markdown2
import os

from xhtml2pdf import pisa
from bundle_dependency import *


class GeneratePdf(PluginHandler):
    async def markdown_to_html(self, markdown_content):
        # convert markdown to html
        html_content = markdown2.markdown(markdown_content)
        return html_content

    async def html_to_pdf(self, html_content, output_pdf, temp_html="temp.html"):
        try:
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_content)

            with open(output_pdf, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

            if pisa_status.err:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Error occurred while generating PDF")
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)

    async def ensure_directory_exists(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            pass

    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        md_content: str = plugin_input.input_params.get("md_content")

        html_content = await self.markdown_to_html(md_content)

        output_pdf = "/mnt/d/Downs/output.pdf"
        await self.ensure_directory_exists(output_pdf)

        await self.html_to_pdf(html_content, output_pdf)

        return PluginOutput(data={"results": output_pdf})
