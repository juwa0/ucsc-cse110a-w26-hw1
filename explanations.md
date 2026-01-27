# HW1-w26

## Part 1

### Correctness: Describe how your scanner extensions implement the required behavior, including any edge cases you handled.

I extended the naive scanner by adding new token checks and changing the ID/NUM scanning loops using only StringStream.peek_char(), eat_char(), and character comparisons (no regex). For SEMI I added a single character match for ;, consuming one character and returning a Lexeme with token SEMI and value ";". For INCR, I implemented ++ by checking for it before returning ADD for +. Since both tokens start with +, the scanner has to prefer the longer match. For ID, I kept the rule that IDs must start witha. lowercase letter, and then I allowed the ID scan loop to continue matching lowercase letters and digits. For NUM, I scanned a run of digits and optionally a single "." followed by at least one digit. If a dot was seen without a digit after it, I raised a ScannerException. I also made sure no NUM token has more than one dot.
### Conceptual: Explain how your implementation aligns with the naive scanner design.

It skips ignored whitespace, tries to match fixed single/multi character operators by simple comparisons, otherwise scans IDs and NUMs using straight-forward loops (consume wihle chars match), and raises ScannerException if valid token can be made. I left the public interface of the scanner unchanged, and the scanner maintains its naive design.

### Experiments: Report your timing results for 10/100/1000/10000 tokens and how you ran them.

I did two separate tests, one with verbose printing on and one with verbose printing off. The results are as follows:
Timing results (no verbose printing):
10 tokens: 8.535385131835938e-05 seconds
100 tokens: 0.0007939338684082031 seconds
1000 tokens: 0.010242938995361328 seconds
10000 tokens: 0.7538061141967773 seconds

Timing results (verbose printing):
10 tokens: 0.00011587142944335938 seconds
100 tokens: 0.0009658336639404297 seconds
1000 tokens: 0.022652864456176758 seconds
10000 tokens: 0.9369869232177734 seconds

### Explanation: Summarize your implementation choices and discuss performance.

I mainly made choices about the implementation for proper ordering and simple scanning. INCR has to be checked before ADD since both start with +. ID scanning has the same naive pattern, just expanded to allow character set after the first letter. NUM scanning adds seen_dot to track if a dot has been seen and keep the rule that a dot must be followed by at least one digit. Performance should scale about linearly with amount of characters/tokens since each character is processed a constant number of times and the new checks are in constant time (one extra lookahead for ++, and a dot check for decimals). 

## Part 2

### Submission: Summarize what you submitted in tokens.py and where it lives in your repo.

Type your answer here.

### Written Report: Describe your RE definitions and include timing results for the EM scanner.

Type your answer here.

### Testing and Verification: Explain how you tested part2.txt (locally and on Gradescope) and report the outcomes.

Type your answer here.

### Debugging and Iteration: Describe any failures you encountered and how you resolved them (include submission iterations if relevant).

Type your answer here.

## Part 3

### Correctness: Describe how your SOS scanner implements the required behavior, including tricky cases.

Type your answer here.

### Conceptual: Explain how your design matches the SOS scanning approach.

Type your answer here.

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the EM scanner.

Type your answer here.

### Explanation: Summarize implementation details and performance observations.

Type your answer here.

## Part 4

### Correctness: Describe how your NG scanner implements the required behavior, including tricky cases.

Type your answer here.

### Conceptual: Explain how your design matches the NG scanning approach.

Type your answer here.

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the SOS scanner.

Type your answer here.

### Explanation: Summarize implementation details and performance observations.

Type your answer here.

