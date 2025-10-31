def distinct_list(lst):
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j and lst[i] == lst[j]:
                    return False
        return True

print(distinct_list([1, 2, 5, 3]))