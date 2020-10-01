from datum_gis.models import Point
from collections import deque


def search_road(p_start, seen):
    new_seen = []
    next_point = []
    new_seen.append(p_start)
    point_start = Point.objects.get(pk=p_start)
    for p in point_start.from_point.values():
        if not p in seen:
            new_seen.append(p['to_point_id'])
            next_point.append(p['to_point_id'])
    return new_seen, next_point


def count_route(point_list, p_end, seen):
    for p in point_list:
        route = []
        if p['to_point_id'] == p_end:
            route.append(p['to_point_id'])
            return route, True
        else:
            point_next = Point.objects.get(pk=p['to_point_id'])
            point_next_list = point_next.from_point.values()
            return count_route(point_next_list, p_end, seen)

#############
start = 2
def djekstra(start):

    Q = deque()
    s = {}
    s[start] = 0
    Q.append(start)
    while Q:
        v = Q.pop()
        point = Point.objects.get(pk=v)
        for u in point.from_point.get_queryset():
            #если линии нет в пути словоря или сумма расстояния меньше, то обновляем очередь
            if u.to_point.id not in s or s[v] + u.distance_line < s[u.to_point.id]:
                s[u.to_point.id] = s[v] + u.distance_line
                Q.append(u.to_point.id)
    return s
