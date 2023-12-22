class Solution(object):
   def strongPasswordChecker(self, s):
      missing_type = 3
      if any('a' <= c <= 'z' for c in s): missing_type -= 1
      if any('A' <= c <= 'Z' for c in s): missing_type -= 1
      if any(c.isdigit() for c in s): missing_type -= 1
      change = 0
      one = two = 0
      p = 2
      while p < len(s):
         if s[p] == s[p-1] == s[p-2]:
            length = 2
            while p < len(s) and s[p] == s[p-1]:
               length += 1
               p += 1
            change += length / 3
            if length % 3 == 0: one += 1
            elif length % 3 == 1: two += 1
         else:
            p += 1
      if len(s) < 6:
         return max(missing_type, 6 - len(s))
      elif len(s) <= 20:
         return max(missing_type, change)
      else:
         delete = len(s) - 20
         change -= min(delete, one)
         change -= min(max(delete - one, 0), two * 2) / 2
         change -= max(delete - one - 2 * two, 0) / 3
         return delete + max(missing_type, change)

pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"what is your name?",
        ["My name is ChatBot."]
    ],
    [
        r"how are you?",
        ["I'm doing well, thanks for asking."]
    ],
    [
        r"what can you do?",
        ["I can chat with you and answer simple questions."]
    ],
    [
        r"bye|goodbye",
        ["Goodbye!", "See you later!"]
    ]
]

