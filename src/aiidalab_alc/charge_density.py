import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import SinglefileData

from aiidalab_alc.common.file_handling import FileUploadWidget

class ChargeDensityStepModel(tl.HasTraits):
    """
    Model for charge density selection.

    A model to define and store required information from the charge density
    step in the app's configuration wizard.
    """

    charge_density_file = tl.Instance(SinglefileData, allow_none=True)
    submitted = tl.Bool(False).tag(sync=True)


    @property
    def has_file(self) -> bool:
        """True if a raw structure file object has been attached to the model."""
        return self.charge_density_file is not None


class ChargeDensityWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """
    Wizard for charge density selection and manipulation.

    A step in a wizard based process widget which allows a user to
    configure a charge density to be used in their workflow.
    """

    def __init__(self, model: ChargeDensityStepModel, **kwargs):
        """
        ChargeDensityWizardStep constructor.

        Parameters
        ----------
        model : ChargeDensityStepModel
            A model controlling the data required for the charge density step.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.rendered = False
        self.model = model

        self.info = ipw.HTML(
            """
                <p>
                    Load in a charge density.
                </p>
            """
        )

        # self.tabs = ipw.Tab()

        # upload file
        # self.tabs.set_title(0, "Upload File")
        self.file_input_widget = ipw.VBox()
        self.file_uploader = FileUploadWidget(description="Charge density file: ")
        self.file_input_widget.children = [
            self.file_uploader,
        ]
        ipw.dlink((self.file_uploader, "file"), (self.model, "charge_density_file"))
    
    def submit_structure(self, _):
        """Submit the structure step."""
        if self.model.has_file or self.model.has_structure:
            self.file_uploader.disable(True)
            self.submit_btn.disabled = True
            self.submit_btn.description = "Submitted"
            self.model.submitted = True
        else:
            self.model.submitted = False
        return
    
    def _update_children(self) -> None:
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
            description="Submit Charge Density file",
            disabled=False,
            button_style="success",
            tooltip="Submit the charge density file to the workflow",
            icon="check",
            layout={"margin": "auto", "width": "60%"},
        )
        self.submit_btn.on_click(self.submit_structure)
        self.viewer = ipw.HTML("<p>No charge density file found...</p>")

        self._update_children()
        self.rendered = True
        return