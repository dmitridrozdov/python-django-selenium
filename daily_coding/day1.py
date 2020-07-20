# Given a list of numbers and a number k, return whether any two numbers from the list add up to k.
# For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.


def calc_for_list_head(lst_head, lst, possible_sum):
    if not lst:
        return False
    else:
        if lst_head + lst[0] == possible_sum:
            return True
        else:
            return calc_for_list_head(lst_head, lst[1:], possible_sum)


def daily1(lst, possible_sum):
    if not lst:
        return False
    else:
        if len(lst) < 2:
            return False
        if calc_for_list_head(lst[0], lst[1:], possible_sum):
            return True
        else:
            return daily1(lst[1:], possible_sum)


if __name__ == '__main__':
    print(daily1([11, 1, 10, 7], 17))