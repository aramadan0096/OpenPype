import pyblish.api
import nuke


class CollectGizmo(pyblish.api.InstancePlugin):
    """Collect Gizmo (group) node instance and its content
    """

    order = pyblish.api.CollectorOrder + 0.22
    label = "Collect Gizmo (group)"
    hosts = ["nuke"]
    families = ["gizmo"]

    def process(self, instance):

        gizmo_node = instance.data["transientData"]["node"]

        # add family to familiess
        instance.data["families"].insert(0, instance.data["family"])
        # make label nicer
        instance.data["label"] = gizmo_node.name()

        # Get frame range
        handle_start = instance.context.data["handleStart"]
        handle_end = instance.context.data["handleEnd"]
        first_frame = int(nuke.root()["first_frame"].getValue())
        last_frame = int(nuke.root()["last_frame"].getValue())

        # Add version data to instance
        version_data = {
            "handles": handle_start,
            "handleStart": handle_start,
            "handleEnd": handle_end,
            "frameStart": first_frame + handle_start,
            "frameEnd": last_frame - handle_end,
            "colorspace": nuke.root().knob('workingSpaceLUT').value(),
            "families": [instance.data["family"]] + instance.data["families"],
            "subset": instance.data["subset"],
            "fps": instance.context.data["fps"]
        }

        instance.data.update({
            "versionData": version_data,
            "frameStart": first_frame,
            "frameEnd": last_frame
        })
        self.log.info("Gizmo instance collected: `{}`".format(instance))
