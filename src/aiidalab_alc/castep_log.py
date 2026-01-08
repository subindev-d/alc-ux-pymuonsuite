import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import SinglefileData

from aiidalab_alc.common.file_handling import FileUploadWidget

class CASTEPLogModel(tl.HasTraits):
    """
    Model for CASTEP log file handling.

    A model to define and store required information from the CASTEP log
    file step in the app's configuration wizard.
    """

    castep_log_file = tl.Instance(SinglefileData, allow_none=True)
    submitted = tl.Bool(False).tag(sync=True)


    @property
    def has_file(self) -> bool:
        """True if a CASTEP log file object has been attached to the model."""
        return self.castep_log_file is not None
    

class CATEPLogWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """
    Wizard for CASTEP log file selection and manipulation.

    A step in a wizard based process widget which allows a user to
    configure a CASTEP log file to be used in their workflow.
    """

    def __init__(self, model: CASTEPLogModel, **kwargs):
        """
        CASTEPLogWizardStep constructor.

        Parameters
        ----------
        model : CASTEPLogModel
            A model controlling the data required for the CASTEP log file step.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.rendered = False
        self.model = model

        self.info = ipw.HTML(
            """
                <p>
                    Load in a CASTEP log file.
                </p>
            """
        )
        
        self.file_input_widget = ipw.VBox()
        self.file_uploader = FileUploadWidget(description="Upload CASTEP log file")
        self.file_input_widget.children = [self.file_uploader]
        ipw.dlink(
            (self.file_uploader, "file"),
            (self.model, "castep_log_file"),
        )
        self.model.observe(self.on_file_upload, "castep_log_file")

    def submit_castep_log(self, _):
        """Submit the uploaded CASTEP log file."""
        if self.model.has_file:
            self.file_uploader.disable(True)
            self.submit_btn.disabled = True
            self.submit_btn.description = "Submitted"
            self.model.submitted = True
        else:
            self.model.submitted = False
        return

    def _update_children(self):
        """Update the widget children to reflect the current state."""
        self.children = [
            self.info,
            self.file_input_widget,
            ipw.HTML("<h2>Viewer:</h2>"),
            self.viewer,
            self.submit_btn,
        ]
        return
    
    def render(self):
        """Render the wizard's contents if not already rendered."""
        if self.rendered:
            return

        self.submit_btn = ipw.Button(
            description="Submit CASTEP Log File",
            disabled=False,
            button_style="success",
            tooltip="Submit the CASTEP log file to the workflow",
            icon="check",
            layout={"margin": "auto", "width": "60%"},
        )
        self.submit_btn.on_click(self.submit_castep_log)
        self.viewer = ipw.HTML("<p>No CASTEP log file found...</p>")

        self._update_children()
        self.rendered = True
        return
    
    def on_file_upload(self, change=None):
        """Handle updates when a new CASTEP log file is uploaded."""
        if self.model.has_file:
            self.viewer.value = f"<p>CASTEP log file '{self.model.castep_log_file.filename}' uploaded successfully.</p>"
        else:
            self.viewer.value = "<p>No CASTEP log file found...</p>"
        return