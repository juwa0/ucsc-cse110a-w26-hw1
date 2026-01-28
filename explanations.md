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

I submitted a finished tokens.py file in the part2 folder of my repo. It defines all required tokens using regular expressions, including identifiers, numbers, hexadecimals, operators, punctuation, and ignored whitespace.

### Written Report: Describe your RE definitions and include timing results for the EM scanner.

ID: [A-Za-z][A-Za-z0-9]*
    This makes sure that identifiers can contain letters and digits but not start with a digit. A token action converts matching lexemes into keyword tokens like IF, ELSE, WHILE, INT, FLOAT when the lexeme value matches a reserved word

NUM: (?:[0-9]+|[0-9]*\.[0-9]+)
    This allows non-negative integers and decimals. If a decimal point show up, at least one digit must follow it.

HNUM: 0[xX][0-9a-fA-F]+ 
    This matches hexadecimal numbers starting with 0x or 0X, followed by one or more hexadecimal digits and it is not case sensitive.

Operators and punctuation (INCR, PLUS, MULT, SEMI, LPAREN, RPAREN, LBRACE, RBRACE, ASSIGN) are matched using exact regular expressions (e.g., \+\+, \+, \*, etc.).

IGNORE: [ \n]+
    This consumes runs of spaces and newlienes so the scanner skips them.

I ran the EMScanner on small test files, since it does exact matching over all substrings, and thus it is slow for big inputs. These are the results:
Part 2 test file: 0.0338139533996582 seconds
10 tokens: 0.009138107299804688 seconds
100 tokens: 1.1023919582366943 seconds

### Testing and Verification: Explain how you tested part2.txt (locally and on Gradescope) and report the outcomes.

I tested part2.txt locally and on Gradescope. The scanner tokenized part2.txt without throwing a ScannerException, and the verbose output showed the correct sequence of tokens in 0.028859853744506836 seconds.
I then submitted the file to Gradescope and it passed all tests!

### Debugging and Iteration: Describe any failures you encountered and how you resolved them (include submission iterations if relevant).

Something I ran into was in NUM edge cases, my initial regex allowed nunmbers like 56,. I fixed this by enforcing at least one digit after the decimal point. After that, I submitted the file to Gradescope and it passed all tests!

## Part 3

### Correctness: Describe how your SOS scanner implements the required behavior, including tricky cases.

The SOS scanner tokenizes by matching only at the start of the remaining string using re.match for every token pattern. On each call to token(), it collects all start-of-string matches and returns the longest one. It also applies the token action so IDs can become keywords and skips IGNORE tokens in a loop. Tricky cases handled correctly include ++ vs + and recognizing keywords like if via the ID token action.

### Conceptual: Explain how your design matches the SOS scanning approach.

This matches the SOS approach because the scanner never checks every substring like the EM scanner. Instead, it only considers token matches anchored at their current position. It then consumes exactly the matched prefix and repeats. 

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the EM scanner.

I timed the SOS scanner locally without -v using:
python3 SOSScanner.py ../tests/test10.txt 
python3 SOSScanner.py ../tests/test100.txt
python3 SOSScanner.py ../tests/test1000.txt
python3 SOSScanner.py ../tests/test10000.txt

Timing results (no verbose printing):
10 tokens: 0.00032711029052734375 seconds
100 tokens: 0.001007080078125 seconds
1000 tokens: 0.008189916610717773 seconds
10000 tokens: 0.13753318786621094 seconds

EMScanner timings:
part2.txt: 0.0338139534 seconds
test10.txt: 0.0091381073 seconds
test100.txt: 1.1023919582 seconds

Speedup examples:
On test10: EM / SOS ≈ 28× faster (0.009138 / 0.000327)
On test100: EM / SOS ≈ ~1095× faster (1.102392 / 0.001007)

The SOS scanner is a lot faster, at around 10 tokens it was almost 30x faster, and at 100 tokens it was neatly 1100x faster!

### Explanation: Summarize implementation details and performance observations.

The main improvement over EMScanner is that the SOSScanner checks each token regex once per call at the start of the string instead of looking through every possible substring with re.fullmatch. Performance-wise, the SOS scanner scales much closer to linearly with input size while the EM scanner grows fast because it repeatedly tests many substrings against all token patterns.

## Part 4

### Correctness: Describe how your NG scanner implements the required behavior, including tricky cases.

Type your answer here.

### Conceptual: Explain how your design matches the NG scanning approach.

Type your answer here.

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the SOS scanner.

Type your answer here.

### Explanation: Summarize implementation details and performance observations.

Type your answer here.

