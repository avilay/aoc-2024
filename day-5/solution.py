from functools import reduce

import networkx as nx


def parse(filename):
    rule_rows, updates = [], []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                if line.find("|") != -1:
                    rule_row = [int(fld) for fld in line.split("|")]
                    rule_rows.append(rule_row)
                else:
                    update = [int(fld) for fld in line.split(",")]
                    updates.append(update)

    return rule_rows, updates


def is_valid(rule_graph, update):
    for i in range(len(update)):
        page = update[i]
        update_followers = update[i + 1:]
        rule_followers = rule_graph[page]
        for update_follower in update_followers:
            if update_follower not in rule_followers:
                return False
    return True


def new_graph(rule):
    graph = {}
    for i in range(len(rule)):
        page = rule[i]
        followers = set(rule[i + 1:])
        graph[page] = followers
    return graph


def consolidate_rule(rules):
    graph = nx.DiGraph()
    graph.add_edges_from(rules)
    return list(nx.topological_sort(graph))


def filter_rules(rule_rows, update):
    uplookup = set(update)
    filtered_rules = list(filter(lambda fs: fs[0] in uplookup and fs[1] in uplookup, rule_rows))
    return filtered_rules


# Answer: 4872
def solve_part_1(rule_rows, updates):
    valid_updates = []
    for update in updates:
        filtered_rules = filter_rules(rule_rows, update)
        rule = consolidate_rule(filtered_rules)
        graph = new_graph(rule)
        if is_valid(graph, update):
            valid_updates.append(update)
    return reduce(lambda acc, pages: acc + pages[len(pages) // 2], valid_updates, 0)


# Answer: 5564
def solve_part_2(rule_rows, updates):
    valid_updates = []
    for update in updates:
        filtered_rules = filter_rules(rule_rows, update)
        rule = consolidate_rule(filtered_rules)
        graph = new_graph(rule)
        if not is_valid(graph, update):
            valid_updates.append(rule)
    return reduce(lambda acc, pages: acc + pages[len(pages) // 2], valid_updates, 0)


def main():
    rule_rows, updates = parse("input.txt")
    # count = solve_part_1(rule_rows, updates)
    count = solve_part_2(rule_rows, updates)
    print(f"Answer: {count}")


if __name__ == '__main__':
    main()
