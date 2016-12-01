from __future__ import absolute_import, division, print_function, unicode_literals

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# readers
from .readers.asvp import Asvp
from .readers.castaway import Castaway
from .readers.digibarpro import DigibarPro
from .readers.digibars import DigibarS
from .readers.elac import Elac
from .readers.idronaut import Idronaut
from .readers.iss import Iss
# from .readers.mvp import Mvp
from .readers.saiv import Saiv
from .readers.seabird import Seabird
from .readers.sippican import Sippican
from .readers.sonardyne import Sonardyne
from .readers.turo import Turo
from .readers.unb import Unb
from .readers.valeport import Valeport

readers = list()
readers.append(Asvp())
readers.append(Castaway())
readers.append(DigibarPro())
readers.append(DigibarS())
readers.append(Elac())
readers.append(Idronaut())
readers.append(Iss())
# readers.append(Mvp())
readers.append(Saiv())
readers.append(Seabird())
readers.append(Sippican())
readers.append(Sonardyne())
readers.append(Turo())
readers.append(Unb())
readers.append(Valeport())

name_readers = list()
ext_readers = list()
desc_readers = list()
for reader in readers:
    name_readers.append(reader.name)
    ext_readers.append(reader.ext)
    desc_readers.append(reader.desc)

# writers
from .writers.asvp import Asvp
from .writers.caris import Caris
from .writers.csv import Csv
from .writers.elac import Elac
from .writers.hypack import Hypack
from .writers.ixblue import Ixblue
from .writers.ncei import Ncei
from .writers.sonardyne import Sonardyne
from .writers.unb import Unb
from .writers.qps import Qps

writers = list()
writers.append(Asvp())
writers.append(Caris())
writers.append(Csv())
writers.append(Elac())
writers.append(Hypack())
writers.append(Ixblue())
writers.append(Ncei())
writers.append(Sonardyne())
writers.append(Unb())
writers.append(Qps())

name_writers = list()
ext_writers = list()
desc_writers = list()
for writer in writers:
    if len(writer.ext):
        name_writers.append(writer.name)
        ext_writers.append(writer.ext)
        desc_writers.append(writer.desc)
