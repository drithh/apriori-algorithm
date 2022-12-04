import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def join_set(item_set, length):
    return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length])


def return_items_with_min_support(item_set, transaction_list, min_support, freq_set):
    _item_set = set()
    local_set = defaultdict(int)

    for item in item_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    for item, count in local_set.items():
        support = float(count)/len(transaction_list)

        if support >= min_support:
            _item_set.add(item)

    return _item_set


def get_item_set_transaction_list(data_iterator):
    transaction_list = list()
    item_set = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transaction_list.append(transaction)
        for item in transaction:
            item_set.add(frozenset([item]))
    return item_set, transaction_list


def run_apriori(data_iter, min_support, min_confidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    return both:
    - items (tuple, support)
    - rules ((pretuple, posttuple), confidence)
    """

    item_set, transaction_list = get_item_set_transaction_list(data_iter)

    freq_set = defaultdict(int)
    large_set = dict()

    one_c_set = return_items_with_min_support(
        item_set, transaction_list, min_support, freq_set)

    current_l_set = one_c_set
    k = 2
    while (current_l_set != set([])):
        large_set[k-1] = current_l_set
        current_l_set = join_set(current_l_set, k)
        current_c_set = return_items_with_min_support(
            current_l_set, transaction_list, min_support, freq_set)
        current_l_set = current_c_set
        k = k + 1

    def get_support(item):
        return float(freq_set[item])/len(transaction_list)

    to_ret_items = []
    for key, value in large_set.items():
        to_ret_items.extend([(tuple(item), get_support(item))
                            for item in value])

    to_ret_rules = []
    for key, value in list(large_set.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item)/get_support(element)
                    if confidence >= min_confidence:
                        to_ret_rules.append(
                            ((tuple(element), tuple(remain)), confidence))
    return to_ret_items, to_ret_rules


def print_results(items, rules):
    for item, support in sorted(items, key=lambda x: x[1]):
        print(f"item: {str(item)} , %.3f" % support)
    print("\n========================== rules:")

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print(f"rule: {str(pre)} -> {str(post)} , %.3f" % confidence)


def results_to_sring(items, rules):
    i, r = [], []
    for item, support in sorted(items, key=lambda x: x[1]):
        i.append(f"item: {str(item)} , %.3f" % support)

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        r.append(f"rule: {str(pre)} -> {str(post)} , %.3f" % confidence)

    return i, r


def data_from_file(filename):
    file_iter = open(filename, newline='')
    for line in file_iter:
        line = line.strip().rstrip(',')
        record = frozenset(line.split(','))
        yield record


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option(
        "-f", "--input_file", dest="input", help="filename containing csv", default=None
    )
    optparser.add_option(
        "-s",
        "--min_support",
        dest="min_s",
        help="minimum support value",
        default=0.01,
        type="float",
    )
    optparser.add_option(
        "-c",
        "--min_confidence",
        dest="min_c",
        help="minimum confidence value",
        default=0.5,
        type="float",
    )

    (options, args) = optparser.parse_args()

    in_file = None
    if options.input is None:
        in_file = sys.stdin
    elif options.input is not None:
        in_file = data_from_file(options.input)
    else:
        print("no dataset filename specified, system with exit\n")
        sys.exit("system will exit")

    min_support = options.min_s
    min_confidence = options.min_c

    items, rules = run_apriori(in_file, min_support, min_confidence)
    print(f"""
        minimum support: {min_support}
        minimum confidence: {min_confidence}
        \n
    """)
    print_results(items, rules)
