from collections import deque

from django.db.models import Q as F

from datum_gis.models import Line


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def get_point_to(line, point_to):
    list_p = [line.to_point.id, line.from_point.id]
    list_p.remove(point_to)
    line_to = list_p[0]
    return line_to


def short_distance(start):

    Q = deque()
    road = {}
    road[start] = float(0)
    Q.append(start)
    while Q:
        v = Q.pop()
        lines = Line.objects.filter(F(from_point_id=v) | F(to_point_id=v))
        for l in lines:
            from_p_id = v
            to_p_id = get_point_to(l, from_p_id)
            if to_p_id not in road or road[v] + l.distance_line < road[to_p_id]:
                road[to_p_id] = round((road[v] + l.distance_line), 2)
                Q.append(to_p_id)
    return road


def short_path(start, end, road):
    v = end
    road_str = {k: str(v) for k, v in road.items()}
    point_path = []
    point_path.append(end)
    while v is not start:
        line = Line.objects.filter(F(from_point_id=v) | F(to_point_id=v))
        for r in line:
            new_distance = str(round((road[v] - r.distance_line), 2))
            if new_distance in road_str.values():
                v = get_key(road_str, new_distance)
                point_path.append(v)
                break

    point_path.reverse()
    show_path = {'distance': road[end], 'points': point_path}
    return show_path


def short_score(start):

    Q = deque()
    road = {}
    road[start] = 0
    Q.append(start)
    while Q:
        v = Q.pop()
        lines = Line.objects.filter(F(from_point_id=v) | F(to_point_id=v))
        for l in lines:
            from_p_id = v
            to_p_id = get_point_to(l, from_p_id)
            if to_p_id not in road or road[v] + l.score < road[to_p_id]:
                road[to_p_id] = road[v] + l.score
                Q.append(to_p_id)
    return road


def short_path_score(start, end, road):
    v = end
    road_str = {k: str(v) for k, v in road.items()}
    point_path = []
    point_path.append(end)
    while v is not start:
        line = Line.objects.filter(F(from_point_id=v) | F(to_point_id=v))
        for r in line:
            new_score = str(round((road[v] - r.score), 2))
            if new_score in road_str.values():
                v = get_key(road_str, new_score)
                point_path.append(v)
                break

    point_path.reverse()
    show_path = {'score': road[end], 'points': point_path}
    return show_path
