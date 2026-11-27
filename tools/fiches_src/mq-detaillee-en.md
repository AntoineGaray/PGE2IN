## What the Drive covers and what is missing

**This sheet does not prepare you for the calculation part of the exam.** The folder holds a single document: chapter 6 of *Keeping Up with the Quants* (Davenport and Kim, Harvard Business Review Press, 2013), titled "Developing Quantitative Analysis Capabilities".

- A calculator is allowed in the exam, so there will probably be calculations (descriptive statistics, probability, tests, regression…). No calculation material is in the Drive.
- This chapter is a "methodology case study": it is about the approach and critical thinking with numbers, not about formulas.
- **Still needed**: the course slides, the tutorials and their answers, and past papers if anyone has them. A formulas-and-methods sheet will follow. Without them, the syllabus could only be guessed.

The English terms below are the chapter's own.

## Davenport and Kim, chapter 6: becoming a proficient quantitative analyst

The chapter's thesis: you become a good analyst through an **attitude** (not being afraid of numbers), **habits** (demanding numbers and being sceptical of them) and **knowledge**, which grow together. It is not first a question of maths level.

### The starting flow chart

The authors start from Aristotle: thoughts → actions → habits → character → destiny. For the analyst, the **quantitative attitude forms your quantitative habits**, and repetition makes the proficient quantitative analyst. Knowledge and methods improve at each stage.

| Stage | What you develop | Related knowledge |
| --- | --- | --- |
| 1. Quantitative attitude | Don't be afraid of numbers, look up unfamiliar terms and numbers, be curious, think probabilistically | Popular statistics books: Huff, *How to Lie with Statistics* (1954); Campbell, *Flaws and Fallacies in Statistical Thinking* (1974); Good and Hardin, *Common Errors in Statistics* |
| 2. Quantitative habits | Demand numbers, never trust numbers, be suspicious of causation arguments, ask questions, practise | Basic statistics and research methods (recommended textbook: Kohler, *Statistics for Business and Economics*). Do every exercise and read it three times |
| 3. Quantitative analyst | Write a report, form a quantitative analysis community, hold seminars regularly | Study real cases in a group, learn advanced methods when you need them, invite experts |

### Stage 1 – The quantitative attitude

- **Don't be afraid of numbers.** Quantitative thinking is different from mathematical knowledge. According to a source quoted in the chapter, being a good quantitative thinker requires very little math beyond sixth-grade level. What counts is extracting information from data.
- **Emily Rosa**: aged 9, she tested "therapeutic touch" (TT), practitioners who claim to feel a patient's energy field. 21 practitioners, 280 trials, **random assignment** of the target hand by coin toss. Result: 122 correct answers, i.e. **44%**, when chance gives **50%**. The claims are therefore unfounded. The study was published in *JAMA* in 1998; she was 11.
- **DJ Patil** (he coined the term *data scientist* at LinkedIn): he failed maths at school, then caught up on his own, all the way to a PhD. The message: a bad start can always be made up.
- **Look up unfamiliar terms**: jot down the terms and numbers you don't understand in the news, then Google them. Within six months, you become the well-informed person around you.
- **Be curious**: Usain Bolt runs 100 m in 9.58 s. Rounding to 10 s, that is 0.1 km in 1/360 of an hour, i.e. about **36 km/h**. The marathon record (2 h 03 min 59 s) works out at about **20.4 km/h**.
- **Think probabilistically**: most adults are "fooled by randomness" (Taleb). They give meaning to events that could easily happen randomly.
    - **The birthday paradox**: with 23 people, the probability that two share a birthday is above 50%.
    - **The random walk** of the stock market: some fund managers beat the market several years in a row, then eventually fall back.
    - **Regression to the mean**: if your income is far above average, your child's income is likely to be lower than yours.
    - Probability is the basis of **inferential statistics**.

### Stage 2 – Quantitative habits

The authors take up the idea that it is easier to act your way into a new way of thinking than to think your way into a new way of acting.

1. **Demand numbers**: faced with an idea or a hunch, ask "Do you have any data to support that hypothesis?". The chapter's line: "The plural of anecdote is not data." Apply the rule to yourself: run a small experiment if the data do not exist.
2. **Never trust numbers**: do not take a figure at face value. It may be manipulated, outdated or drawn from a non-representative sample. Three angles of doubt:
    - **Relevance**: does the figure answer the question, and does it represent the target group?
    - **Accuracy**: who produced it, and how?
    - **Correct interpretation**: the same figure can be read two ways. Example: "only one wife in 22 votes differently from her husband" can also read "only one husband in 22 has the courage to vote against his wife".
3. **Be particularly suspicious of causation arguments**: **correlation is not causation**. Only an experiment with a test group, a control group and random assignment allows a causal conclusion. Chabris and Simons's test (*The Invisible Gorilla*): could people have been assigned randomly to one of the conditions? If that is impossible, too expensive or unethical, the study is not an experiment and causation is not proven. Example: "heavy drinking causes cancer", when heavy drinkers may also be heavy smokers (a hidden variable). The fallacy has a name: *cum hoc ergo propter hoc* (A is correlated with B, therefore A causes B).
4. **Ask questions**: faced with an **average**, ask about the spread (the **standard deviation**), **outliers**, missing data and the **median**. Faced with a **survey**, ask who ran it, how, and how the questions were worded.
5. **Practice quantitative analyses**: go through the six steps of analysis on real problems.

### The 10 questions to ask about a quantitative analysis

1. Do you have any data to support that hypothesis?
2. What is the source of the data used in the analysis?
3. Is the sample data representative of the population?
4. Are there outliers in the data distribution, and how did they affect the results?
5. What assumptions are behind the analysis?
6. Are there conditions that would make the assumptions and the model invalid?
7. Why was that particular approach to analysis chosen?
8. What transformations of the data were needed to get the model to fit well?
9. Were other approaches to analysing the data considered, and why were they rejected?
10. How likely is it that the independent variables are really causing the changes in the dependent variable? Could more analysis be done on causation?

### The 6 steps of a quantitative analysis

1. **Problem recognition** (and framing): understand what the problem is and why it matters. This step determines which statistical method will be used later.
2. **Review of previous findings**: look for existing work, identify the relevant variables and how they relate. According to the authors, a well-defined question and a well-reviewed literature are more than half the work.
3. **Modeling (variable selection)**: drop the variables that do not help solve the problem, as if drawing a caricature. The choice depends on the purpose. For a toy train, the scale of an actual train matters. For the economic feasibility of a real train, it is tonnage, speed and fuel consumption.
4. **Data collection (measurement)**: first check whether the data already exist, internally or publicly. Buying data is almost always cheaper than collecting it. Otherwise, take care over survey design (question wording) or consult a specialist for an experiment.
5. **Data analysis**: look for patterns and relationships between variables. To **compare groups**, use comparison tests. For a **dependence relationship** between variables, use **regression**.
6. **Results presentation and action**: spend as much time on it as on the other five steps. Learn data visualisation, with Edward Tufte's books as the reference.

### Stage 3 – The quantitative analyst

- **Write a report** to learn to "tell a story with data". Three aims: progress by tackling a real problem, help solve a company problem, spread an analytical culture. Choose the question carefully: as Voltaire said, people judge you by your questions rather than by your answers.
- **Form a quantitative analysis community**: prioritise topics, share out the six steps, present work to each other. Henry Ford's quote on coming together, keeping together and working together.
- **Hold seminars regularly**, some of them accessible to nontechnical people.

### The two final examples, analysed with the 6 steps

**Nuri and the scholarship** ("Scholarship Made Easy"). Jinho Kim analysed how his daughters could get a PhD scholarship in the United States. In research, the professor runs steps 1 to 3 and the writing. PhD students mostly do data collection (4) and data analysis (5), the longest steps. Nuri therefore prepared exactly for those: statistics and research methods courses, SPSS software training, a critical reading of 20 recent papers. Result: a scholarship at Wisconsin, then a fellowship at Stanford. Her sister got a fellowship at Michigan.

**Daryl Morey and Shane Battier (Houston Rockets).** Morey is "the Billy Beane of professional basketball", a reference to *Moneyball*.

| Step | Application |
| --- | --- |
| 1. Problem recognition | Should the team acquire Battier, whose individual statistics are weak? |
| 2. Review of previous findings | Sports analytics work well when individual performance explains team performance, but that is harder in basketball. Battier averaged around 10 points and fewer than 5 rebounds per game, yet his team played better when he was on the court |
| 3. Modeling | Acquisition cost, salary, individual statistics, and above all the team's performance with and without him |
| 4. Data collection | The **plus/minus** statistic: how the team performs when the player is on the court, compared with when he is on the bench |
| 5. Data analysis | A **regression-adjusted** plus/minus of **+8** in 2006-2007, 17th in the league, for an average salary. The player he was traded for ranked 45th |
| 6. Results presentation and action | The trade is made. The Rockets go from 34-48 to 52-30 (2007-2008), then 55-27 with a 22-game winning streak. Battier later wins the NBA title with Miami in 2012 |

### Likely exam questions on this text

These are hypotheses, not confirmed topics.

- Apply the 6 steps to a given case (the most likely).
- Explain why a correlation does not prove causation, and what would be needed to prove it.
- List the questions to ask about an average or a survey.
- Interpret Emily Rosa's experiment: why 44% proves nothing, and why random assignment matters.
- A small conversion or probability calculation, in the spirit of the Usain Bolt example or the birthday paradox.
