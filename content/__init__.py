# 전체 페이지 목록 집계
from . import (main, areas, dongs_bongcheon, dongs_sillim, dongs_namhyeon,
               stations, livingareas, themes, info, magazine, about)

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + dongs_bongcheon.PAGES
    + dongs_sillim.PAGES
    + dongs_namhyeon.PAGES
    + stations.PAGES
    + livingareas.PAGES
    + themes.PAGES
    + info.PAGES
    + magazine.PAGES
    + [about.PAGE]
)
