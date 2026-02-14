import pcbnew
import os
import wx


def debug(msg):
    wx.MessageBox(str(msg), "Debug Message", wx.OK)


class AlignGridAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Align To Grid"
        self.category = "Modify PCB"
        self.description = "Align selected items to the grid"
        self.show_toolbar_button = True  # Optional, defaults to False
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), 'icon.png')  # Optional

    def Run(self):
        # default grid size
        GRID_SIZE = 50  # default grid size

        # get grid size from user
        dlg = wx.TextEntryDialog(
            None, "Enter grid size (mil)", "Grid Size", str(GRID_SIZE))
        if dlg.ShowModal() == wx.ID_OK:
            try:
                GRID_SIZE = int(dlg.GetValue())
            except ValueError:
                print("Invalid grid size")
                return

        # get all footprints
        footprints = pcbnew.GetBoard().GetFootprints()

        # filter selected footprints
        selected = [i for i in footprints if i.IsSelected()]

        # check if no footprints are selected
        if not selected:
            print("No footprints selected")
            return

        # move selected footprints to defined grid points
        for footprint in selected:
            position = (footprint.GetPosition().x, footprint.GetPosition().y)
            position = (pcbnew.PutOnGridMils(i, GRID_SIZE) for i in position)
            footprint.SetPosition(pcbnew.VECTOR2I(*position))
