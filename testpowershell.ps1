docker pull simgrid/tuto-s4u
docker run -it --rm --name simgrid --volume ~/simgrid-tutorial:/source/tutorial simgrid/tuto-s4u bash
cd /source/tutorial
python master-workers.py small_platform.xml master-workers_d.xml