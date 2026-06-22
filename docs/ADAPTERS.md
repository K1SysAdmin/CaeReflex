# ADAPTERS

AdapterResult contract. GmshAdapter inspects .geo in core and .msh with [mesh]. OpenFOAMAdapter inspects text dictionaries without OpenFOAM installation. VTKAdapter fingerprints VTK-family files and inspects tiny legacy .vtk files in core. New adapters must return AdapterResult and must not write directly to reports or REST responses.
