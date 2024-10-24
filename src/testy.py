import re

t_string = "23.2%O2,22.9C,1099mB"
regex_o2 = "^[0-9]*\.[0-9]*"
regex_te = "[0-9]*\.[0-9]*\B"
regex_pr = "[0-9]{4}|[0-9]{3}"

o2 = re.search(regex_o2, t_string).group()
te = re.search(regex_te, t_string).group()
pr = re.search(regex_pr, t_string).group()

print("Found "+o2+":"+te+":"+pr)
