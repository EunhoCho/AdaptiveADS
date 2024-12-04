import json
import csv

ROUTE = "longest6"
AGENTS = ["basic", "transfuser", "hybrid"]
FILES = [0, 0, 0]
SCORE_TYPE = ["route", "penalty", "composed"]
INFRACTION_TYPE = ["collision_layout", "collision_pedestrian", "collision_vehicle", "outside_route", "red_light",
                   "route_dev", "route_timeout", "stop_infraction", "vehicle_blocked"]


class AgentRecord:
    def __init__(self, record_objects):
        self.record_objects = record_objects

    def avg_score(self, score_type):
        score = 0
        for record in self.record_objects:
            if score_type == "route":
                score += record.score_route
            elif score_type == "penalty":
                score += record.score_penalty
            elif score_type == "composed":
                score += record.score_composed
            else:
                raise Exception("Unknown score type")
        return score / len(self.record_objects)

    def num_infraction(self, infraction_type):
        infractions = 0
        for record in self.record_objects:
            if infraction_type == "collision_layout":
                infractions += 1 if record.collision_layout else 0
            elif infraction_type == "collision_pedestrian":
                infractions += 1 if record.collision_pedestrian else 0
            elif infraction_type == "collision_vehicle":
                infractions += 1 if record.collision_vehicle else 0
            elif infraction_type == "outside_route":
                infractions += 1 if record.outside_route else 0
            elif infraction_type == "red_light":
                infractions += 1 if record.red_light else 0
            elif infraction_type == "route_dev":
                infractions += 1 if record.route_dev else 0
            elif infraction_type == "route_timeout":
                infractions += 1 if record.route_timeout else 0
            elif infraction_type == "stop_infraction":
                infractions += 1 if record.stop_infraction else 0
            elif infraction_type == "vehicle_blocked":
                infractions += 1 if record.vehicle_blocked else 0
            else:
                raise Exception("Unknown infraction type")
        return infractions

    def time_ratio(self):
        duration_game = 0
        duration_system = 0

        for record in self.record_objects:
            duration_game += record.duration_game
            duration_system += record.duration_system

        return duration_game / duration_system


class Record:
    def __init__(self, score_route, score_penalty, score_composed, collision_layout, collision_pedestrian,
                 collision_vehicle, outside_route, red_light, route_dev, route_timeout, stop_infraction,
                 vehicle_blocked, duration_game, duration_system):
        self.score_route = score_route
        self.score_penalty = score_penalty
        self.score_composed = score_composed
        self.collision_layout = collision_layout
        self.collision_pedestrian = collision_pedestrian
        self.collision_vehicle = collision_vehicle
        self.outside_route = outside_route
        self.red_light = red_light
        self.route_dev = route_dev
        self.route_timeout = route_timeout
        self.stop_infraction = stop_infraction
        self.vehicle_blocked = vehicle_blocked
        self.duration_game = duration_game
        self.duration_system = duration_system

    def has_infraction(self):
        if (self.collision_layout or self.collision_pedestrian or self.collision_vehicle or self.outside_route or
                self.red_light or self.route_dev or self.route_timeout or self.stop_infraction or self.vehicle_blocked):
            return True
        return False


if __name__ == "__main__":
    agent_data = {}
    agent_records = {}

    for i, agent in enumerate(AGENTS):
        if FILES[i] == 0:
            with open("results/" + agent + "_" + ROUTE + ".json", "r") as f:
                data = json.load(f)
                agent_data[agent] = data['_checkpoint']['records']
                progress = data['_checkpoint']['progress'][0]
        else:
            with open("results/" + agent + "_" + ROUTE + "_1.json", "r") as f:
                data = json.load(f)['_checkpoint']['records']

            for j in range(2, FILES[i] + 1):
                with open("results/" + agent + "_" + ROUTE + "_" + str(j) + ".json", "r") as f:
                    data_2 = json.load(f)['_checkpoint']['records']
                    data += data_2

            agent_data[agent] = data

    targets = []
    for scenario in agent_data[AGENTS[0]]:
        targets.append(int(scenario['route_id'].split('_')[1]))
    max_targets = targets[:]

    for agent in AGENTS[1:]:
        new_targets = []
        for scenario in agent_data[agent]:
            new_targets.append(int(scenario['route_id'].split('_')[1]))
        max_targets += new_targets

        for target in targets[:]:
            if target not in new_targets:
                targets.remove(target)

    print("FOR SCENARIO", len(targets), "AMONG", len(set(max_targets)))
    print(targets)
    print()

    for agent in AGENTS:
        records = agent_data[agent]

        target_records = []
        for record in records:
            if int(record['route_id'].split('_')[1]) in targets:
                target_records.append(record)

        record_objects = []
        for record in target_records:
            score = record['scores']
            infractions = record['infractions']
            meta = record['meta']
            record_objects.append(Record(score['score_route'],
                                         score['score_penalty'],
                                         score['score_composed'],
                                         len(infractions['collisions_layout']) > 0,
                                         len(infractions['collisions_pedestrian']) > 0,
                                         len(infractions['collisions_vehicle']) > 0,
                                         len(infractions['outside_route_lanes']) > 0,
                                         len(infractions['red_light']) > 0,
                                         len(infractions['route_dev']) > 0,
                                         len(infractions['route_timeout']) > 0,
                                         len(infractions['stop_infraction']) > 0,
                                         len(infractions['vehicle_blocked']) > 0,
                                         meta['duration_game'],
                                         meta['duration_system']))

        agent_records[agent] = AgentRecord(record_objects)

    with open("results/" + ROUTE + ".csv", 'w', newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([''] + AGENTS)

        print("SCORE ANALYSIS")
        for score_type in SCORE_TYPE:
            print("SCORE TYPE:", score_type)
            row = [score_type]
            for agent in AGENTS:
                score = agent_records[agent].avg_score(score_type)
                print("Agent:", agent, "=", score)
                row.append(score)
            print()
            csv_writer.writerow(row)

        print("INFRACTION ANALYSIS")
        for infraction_type in INFRACTION_TYPE:
            row = [infraction_type]
            print("INFRACTION TYPE:", infraction_type)
            for agent in AGENTS:
                num = agent_records[agent].num_infraction(infraction_type)
                print("Agent:", agent, "=", num)
                row.append(num)
            print()
            csv_writer.writerow(row)

        print("TIME RATIO ANALYSIS")
        row = ['time_ratio']
        for agent in AGENTS:
            ratio = agent_records[agent].time_ratio()
            print("Agent:", agent, "=", ratio)
            row.append(ratio)
        csv_writer.writerow(row)
