"""
study_expert.py  -  THE BRAIN of the Study Method Finder

This file has NO screen code. It only contains the "expert knowledge":

    1. METHODS        the study methods we can recommend
    2. OPTIONS        the answers a user can pick for each question
    3. find_methods() the 55 IF-THEN rules that pick the best methods

HOW IT WORKS (in plain words)
    - The user answers 13 questions. Each answer is a "fact".
    - We check 55 rules. A rule looks like this:
          IF the subject is Memorization
          THEN give 3 points to "Active Recall"
    - Every rule that is true adds points to a study method.
    - The methods with the most points are the best advice.

The screen (buttons, questions, results) is in app.py.
To test only this file, run:   python study_expert.py
"""

# Facts about this rule base (used on the screen)
TOTAL_RULES = 55
TOTAL_CONDITIONS = 66      # 55 rules, and 11 of them test two things at once


# =====================================================================
# PART 1: THE STUDY METHODS
# Each method has:  "info"  = a short explanation
#                   "steps" = 3 steps that tell the user how to do it
# =====================================================================
METHODS = {
    "Spaced Repetition": {
        "info": "Review the same material at growing gaps (1 day, 3 days, 7 days) so it moves into long-term memory.",
        "steps": ["Put key facts on flashcards (paper or an app like Anki).",
                  "Review them today, then after 1, 3, 7 and 14 days.",
                  "Remove cards you always get right. Repeat the ones you miss."],
    },
    "Active Recall (Flashcards)": {
        "info": "Test yourself instead of re-reading. Pulling facts out of your head is what builds memory.",
        "steps": ["Close the book and write down everything you remember.",
                  "Check what you missed and make flashcards for those gaps.",
                  "Quiz yourself every day until you stop missing them."],
    },
    "Practice Problems": {
        "info": "Solve many problems yourself. You learn problem solving by solving, not by watching.",
        "steps": ["Try each problem alone for 5-10 minutes before looking at the answer.",
                  "Keep an 'error log' of your mistakes and why you made them.",
                  "Redo the problems you got wrong after 2-3 days."],
    },
    "Timed Mock Exams": {
        "info": "Practice with past papers under real exam conditions (time limit, no notes).",
        "steps": ["Find 2-3 past papers or sample tests.",
                  "Set a timer and finish the paper without any help.",
                  "Mark it honestly and study only the questions you lost marks on."],
    },
    "Feynman Technique": {
        "info": "Explain the topic in simple words, as if teaching a child. Where you get stuck is what you don't understand yet.",
        "steps": ["Write the topic at the top of a blank page.",
                  "Explain it in plain language without looking at your notes.",
                  "Go back to the book for the parts you couldn't explain, then repeat."],
    },
    "Mind Maps": {
        "info": "Draw the topic like a tree: main idea in the center, branches for sub-topics. Shows how ideas connect.",
        "steps": ["Write the main topic in the center of a page.",
                  "Add a branch for each sub-topic, then small branches for details.",
                  "Use colors and drawings, then redraw it from memory."],
    },
    "Cornell Notes": {
        "info": "A note layout with a notes column, a question column and a summary box.",
        "steps": ["Draw a line: left 1/3 for questions, right 2/3 for notes, a box at the bottom.",
                  "Write notes on the right and questions on the left.",
                  "Cover the notes and answer the questions to test yourself."],
    },
    "Outline and Practice Essays": {
        "info": "Plan the structure first, then write timed practice paragraphs or essays.",
        "steps": ["Write a 5-point outline (intro, 3 main points, conclusion).",
                  "Write an essay or a few paragraphs in a fixed time.",
                  "Compare with a model answer and fix weak arguments."],
    },
    "Record and Listen": {
        "info": "Say your notes out loud, record them and listen back. Great if you learn by hearing.",
        "steps": ["Read your summary aloud into a voice recorder.",
                  "Listen while walking or travelling.",
                  "Pause and try to say the next sentence before it plays."],
    },
    "Study Group Discussion": {
        "info": "Study with friends: explain topics to each other and quiz one another.",
        "steps": ["Pick 3-4 people and choose one topic per session.",
                  "Take turns explaining a sub-topic to the group.",
                  "Finish with 10 minutes of quick quiz questions."],
    },
    "Learn by Doing": {
        "info": "Turn the material into something you can do: experiments, mini-projects, examples.",
        "steps": ["For each topic ask: 'What could I build or try with this?'",
                  "Do a small experiment, project or demo.",
                  "Write down what worked and what didn't."],
    },
    "Pomodoro Technique": {
        "info": "Study in short focused sprints with short breaks. Easy on your attention.",
        "steps": ["Set a timer for 25 minutes (or 15 if that is too long for you).",
                  "Work on one task only until the timer rings.",
                  "Take a 5-minute break. After 4 rounds take a 20-minute break."],
    },
    "Study Planner (Time Blocking)": {
        "info": "Schedule fixed study blocks in your calendar so you don't have to decide when to start.",
        "steps": ["List all topics and your exam date.",
                  "Give each topic a fixed time slot each day.",
                  "Feeling lazy? Start with just 10 minutes. Starting is the hardest part."],
    },
    "Last-Minute Priority Plan": {
        "info": "With very little time, don't try to cover everything. Focus on the most important topics.",
        "steps": ["List topics and mark the ones most likely to appear in the exam.",
                  "Study the top 30% of topics first using active recall.",
                  "Sleep well the night before. A tired brain remembers less."],
    },
    "Relaxation + Exam Rehearsal": {
        "info": "Reduce nerves by making the exam feel familiar and by calming your body first.",
        "steps": ["Do practice tests in a similar setting (desk, timer, silence).",
                  "Before you start, breathe in for 4 seconds and out for 6 seconds, 5 times.",
                  "Tell yourself 'I have done this before', because in practice you have."],
    },
    "Mnemonics (Memory Tricks)": {
        "info": "Turn hard facts into a rhyme, acronym or funny picture so they are easier to remember.",
        "steps": ["Make an acronym from the first letters of a list (like ROYGBIV for rainbow colors).",
                  "Or link each fact to a silly, vivid image in your mind.",
                  "Say your trick out loud and test yourself the next day."],
    },
    "Clean Up Your Notes": {
        "info": "Messy notes slow you down. Rewrite them into short, clear summaries before studying.",
        "steps": ["Read your notes and cross out anything that is not important.",
                  "Rewrite each topic as 3-5 short bullet points.",
                  "Use this clean version for flashcards and revision."],
    },
    "SQ3R Reading Method": {
        "info": "A way to study a textbook actively: Survey, Question, Read, Recite, Review.",
        "steps": ["Survey: skim the headings and summary of the chapter first.",
                  "Question: turn each heading into a question, then Read to answer it.",
                  "Recite the answers in your own words, then Review at the end."],
    },
    "Practice Quizzes (Multiple Choice)": {
        "info": "Answer many multiple-choice questions to get used to the style and spot tricky options.",
        "steps": ["Find or make 20-30 multiple-choice questions per topic.",
                  "Cover the options and try to answer before looking.",
                  "For every wrong answer, write down why the right option is right."],
    },
    "Oral Practice (Speak Out Loud)": {
        "info": "Practice saying answers or sentences aloud. Speaking is a skill you only build by speaking.",
        "steps": ["Pick a topic and explain it out loud for 2 minutes.",
                  "Record yourself or practice with a friend.",
                  "Listen back and fix mistakes and long pauses."],
    },
    "Distraction-Free Setup": {
        "info": "Remove the things that pull your attention away before you start studying.",
        "steps": ["Put your phone in another room or turn on Do Not Disturb.",
                  "If it is noisy, use earplugs or headphones with calm music.",
                  "Clear your desk. Keep only what you need for this session."],
    },
    "Beginner Step-by-Step Path": {
        "info": "If the topic is new, start with the basics and build up slowly instead of jumping to hard parts.",
        "steps": ["List the topics from easiest to hardest.",
                  "Read or watch a beginner summary of each one.",
                  "Move to the next topic only when you can explain the current one."],
    },
    "Deep Work Sessions": {
        "info": "Long, uninterrupted blocks (45-90 minutes) for hard topics. Best when you can concentrate for a long time.",
        "steps": ["Choose one hard topic and one clear goal.",
                  "Work for 45-90 minutes with no phone and no extra tabs.",
                  "Then take a proper 15-minute break."],
    },
    "Goals and Rewards": {
        "info": "Set small daily goals and reward yourself when you finish them. It builds the habit of starting.",
        "steps": ["Write 2-3 small goals for today (like 'finish 10 questions').",
                  "Choose a reward (tea, a short video, a walk) for after you finish.",
                  "Tick the goals off on paper and watch your streak grow."],
    },
}


# =====================================================================
# PART 2: THE ANSWER CHOICES
# For each question, the list of answers the user can pick from.
# The rules in PART 3 use these exact words.
# =====================================================================
OPTIONS = {
    "subject":   ["Memorization", "Problem solving", "Concepts and theory", "Writing", "Language learning"],
    "exam":      ["Multiple choice", "Written answers", "Practical or lab", "Oral exam"],
    "level":     ["Beginner", "Intermediate", "Advanced"],
    "notes":     ["I have good notes", "My notes are messy", "I only have a textbook"],
    "time_left": ["1-2 days", "Less than 1 week", "1-4 weeks", "More than 1 month"],
    "hours":     ["Less than 1 hour", "1 to 3 hours", "More than 3 hours"],
    "best_time": ["Morning", "Afternoon", "Night"],
    "style":     ["Visual", "Auditory", "Reading and writing", "Hands-on"],
    "struggle":  ["Getting distracted", "Forgetting quickly", "Not understanding", "Procrastinating", "Exam nerves"],
    "focus":     ["Under 15 minutes", "15 to 30 minutes", "More than 30 minutes"],
    "phone":     ["Yes, a lot", "Sometimes", "Rarely"],
    "place":     ["Quiet room", "Library", "Noisy home", "On the go (bus, travel)"],
    "company":   ["Alone", "With other people"],
}


# =====================================================================
# PART 3: THE RULES AND THE ENGINE
#
# find_methods() takes the user's answers and returns the study methods
# sorted from best to worst.
#
# Every rule has this shape:
#
#     if <condition>:
#         add(rule number, method, points, reason)
#
# "points" = how strongly the rule recommends the method (1 = weak, 3 = strong)
# =====================================================================
def find_methods(answers):
    """
    answers : a dictionary like {"subject": "Writing", "exam": "Oral exam", ...}

    returns : a list, best method first. Each item looks like:
              {"method": "Pomodoro Technique",
               "score": 8,
               "reasons": ["Rule 24 (+3): Short focused sprints help ..."]}
    """

    # ----- Step 1: read the answers into simple variables -----
    subject = answers["subject"]
    exam = answers["exam"]
    level = answers["level"]
    notes = answers["notes"]
    time_left = answers["time_left"]
    hours = answers["hours"]
    best_time = answers["best_time"]
    style = answers["style"]
    struggle = answers["struggle"]
    focus = answers["focus"]
    phone = answers["phone"]
    place = answers["place"]
    company = answers["company"]

    # ----- Step 2: two notebooks to remember what happened -----
    scores = {}    # method name -> total points so far
    reasons = {}   # method name -> list of reasons so far

    def add(rule_number, method, points, why):
        """Called by a rule that is TRUE: give points to a method and remember why."""
        if method not in scores:        # first time we see this method
            scores[method] = 0
            reasons[method] = []
        scores[method] = scores[method] + points
        reasons[method].append(f"Rule {rule_number} (+{points}): {why}")

    # A shortcut used by two rules: True when the exam is close
    short_time = time_left in ["1-2 days", "Less than 1 week"]

    # ----- Step 3: the 55 rules -----

    # ---------- Rules about the SUBJECT (rules 1-14) ----------
    if subject == "Memorization" and time_left == "More than 1 month":
        add(1, "Spaced Repetition", 3, "You have lots of time, and memorizing works best when spread out")

    if subject == "Memorization" and time_left == "1-4 weeks":
        add(2, "Spaced Repetition", 2, "A few weeks is enough to benefit from spaced review")

    if subject == "Memorization":
        add(3, "Active Recall (Flashcards)", 3, "Memorization improves most when you test yourself")

    if subject == "Memorization":
        add(4, "Mnemonics (Memory Tricks)", 2, "Memory tricks make facts easier to remember")

    if subject == "Problem solving":
        add(5, "Practice Problems", 3, "Problem-solving skill only comes from solving problems")

    if subject == "Problem solving" and short_time:
        add(6, "Timed Mock Exams", 3, "Your exam is close, so practice under exam conditions")

    if subject == "Concepts and theory":
        add(7, "Feynman Technique", 3, "Concept subjects need real understanding, and explaining simply tests that")

    if subject == "Concepts and theory" and style == "Visual":
        add(8, "Mind Maps", 3, "Mind maps show how concepts connect, and you learn visually")

    if subject == "Concepts and theory" and style == "Reading and writing":
        add(9, "Cornell Notes", 2, "You like reading and writing, and Cornell notes turn notes into self-tests")

    if subject == "Concepts and theory" and company == "With other people":
        add(10, "Study Group Discussion", 2, "Discussing concepts with others shows gaps in your understanding")

    if subject == "Writing":
        add(11, "Outline and Practice Essays", 3, "Writing improves by planning and practicing writing")

    if subject == "Language learning":
        add(12, "Spaced Repetition", 3, "Vocabulary sticks best with spaced review")

    if subject == "Language learning":
        add(13, "Oral Practice (Speak Out Loud)", 3, "A language is learned by speaking it")

    if subject == "Language learning" and style == "Auditory":
        add(14, "Record and Listen", 2, "You learn by hearing, which is perfect for languages")

    # ---------- Rules about TIME LEFT (rules 15-18) ----------
    if time_left == "1-2 days":
        add(15, "Last-Minute Priority Plan", 3, "With only 1-2 days, you must pick the most important topics")

    if short_time:
        add(16, "Active Recall (Flashcards)", 2, "When time is short, testing yourself is the fastest way to learn")

    if time_left == "1-4 weeks":
        add(17, "Study Planner (Time Blocking)", 2, "A few weeks need a clear plan")

    if time_left == "More than 1 month":
        add(18, "Study Planner (Time Blocking)", 1, "A long runway needs a plan so you don't waste it")

    # ---------- Rules about LEARNING STYLE (rules 19-23) ----------
    if style == "Visual":
        add(19, "Mind Maps", 1, "Visual learners usually like diagrams and colors")

    if style == "Auditory":
        add(20, "Record and Listen", 2, "You learn by hearing, so listen to your own recorded notes")

    if style == "Auditory" and company == "With other people":
        add(21, "Study Group Discussion", 2, "You learn by hearing and talking, and groups are perfect for that")

    if style == "Reading and writing":
        add(22, "Cornell Notes", 1, "You like reading and writing, so structured notes suit you")

    if style == "Hands-on":
        add(23, "Learn by Doing", 2, "You learn best by doing, so turn topics into practice tasks")

    # ---------- Rules about the BIGGEST STRUGGLE (rules 24-32) ----------
    if struggle == "Getting distracted":
        add(24, "Pomodoro Technique", 3, "Short focused sprints help when your attention drifts")

    if struggle == "Forgetting quickly":
        add(25, "Active Recall (Flashcards)", 2, "Forgetting is fixed by pulling information out again and again")

    if struggle == "Forgetting quickly":
        add(26, "Spaced Repetition", 2, "Reviewing at growing gaps fights forgetting")

    if struggle == "Not understanding":
        add(27, "Feynman Technique", 2, "Explaining simply shows exactly which part you don't understand")

    if struggle == "Not understanding" and level == "Beginner":
        add(28, "Beginner Step-by-Step Path", 3, "You are new to this, so build up from the basics")

    if struggle == "Procrastinating":
        add(29, "Study Planner (Time Blocking)", 3, "Fixed time slots remove the 'when should I start?' decision")

    if struggle == "Procrastinating":
        add(30, "Goals and Rewards", 2, "Small goals with rewards make starting easier")

    if struggle == "Exam nerves":
        add(31, "Relaxation + Exam Rehearsal", 3, "Practicing in exam-like conditions makes the real exam feel familiar")

    if struggle == "Exam nerves":
        add(32, "Timed Mock Exams", 2, "Mock exams build confidence")

    # ---------- Rule about STUDYING ALONE or WITH OTHERS (rule 33) ----------
    if company == "With other people":
        add(33, "Study Group Discussion", 1, "You said you like studying with other people")

    # ---------- Rules about HOURS PER DAY (rules 34-35) ----------
    if hours == "Less than 1 hour":
        add(34, "Active Recall (Flashcards)", 2, "With little time per day, testing yourself is the most efficient method")

    if hours == "More than 3 hours":
        add(35, "Pomodoro Technique", 2, "Long study days need regular breaks to avoid burnout")

    # ---------- Rules about the BEST TIME OF DAY (rules 36-38) ----------
    if best_time == "Morning" and subject == "Problem solving":
        add(36, "Practice Problems", 1, "Hard problems are best solved when your mind is fresh in the morning")

    if best_time == "Night" and subject == "Memorization":
        add(37, "Spaced Repetition", 1, "Reviewing before sleep helps memory")

    if best_time == "Afternoon":
        add(38, "Pomodoro Technique", 1, "Short sprints help during the afternoon energy dip")

    # ---------- Rules about CONCENTRATION SPAN (rules 39-41) ----------
    if focus == "Under 15 minutes":
        add(39, "Pomodoro Technique", 3, "You focus for a short time, so use short sprints (try 15 minutes)")

    if focus == "15 to 30 minutes":
        add(40, "Pomodoro Technique", 2, "Your focus time fits the 25-minute sprint very well")

    if focus == "More than 30 minutes":
        add(41, "Deep Work Sessions", 2, "You can focus for a long time, so use long blocks")

    # ---------- Rules about the STUDY PLACE (rules 42-44) ----------
    if place == "Noisy home":
        add(42, "Distraction-Free Setup", 3, "A noisy place needs a setup that blocks distractions")

    if place == "Library":
        add(43, "Deep Work Sessions", 1, "A library is a great place for long, focused sessions")

    if place == "On the go (bus, travel)":
        add(44, "Record and Listen", 2, "Audio is easy to study while travelling")

    # ---------- Rules about PHONE DISTRACTION (rules 45-46) ----------
    if phone == "Yes, a lot":
        add(45, "Distraction-Free Setup", 3, "Your phone is a big distraction, so remove it from the room")

    if phone == "Yes, a lot":
        add(46, "Pomodoro Technique", 2, "A timer gives you a clear phone-free period")

    # ---------- Rules about your LEVEL (rules 47-48) ----------
    if level == "Beginner":
        add(47, "Beginner Step-by-Step Path", 3, "As a beginner, start with the basics and build up")

    if level == "Advanced":
        add(48, "Timed Mock Exams", 2, "You know the subject well, so test yourself with real exam practice")

    # ---------- Rules about the EXAM TYPE (rules 49-52) ----------
    if exam == "Multiple choice":
        add(49, "Practice Quizzes (Multiple Choice)", 3, "Practice with the same question style as your exam")

    if exam == "Written answers":
        add(50, "Outline and Practice Essays", 2, "Written exams need practice writing answers")

    if exam == "Practical or lab":
        add(51, "Learn by Doing", 3, "A practical exam tests what you can do, so practice doing it")

    if exam == "Oral exam":
        add(52, "Oral Practice (Speak Out Loud)", 3, "An oral exam needs practice speaking your answers")

    # ---------- Rules about your NOTES (rules 53-55) ----------
    if notes == "My notes are messy":
        add(53, "Clean Up Your Notes", 3, "Clean notes make every other method easier")

    if notes == "I only have a textbook":
        add(54, "SQ3R Reading Method", 3, "A textbook needs an active reading method")

    if notes == "I have good notes":
        add(55, "Active Recall (Flashcards)", 1, "Good notes can be turned into questions and flashcards")

    # ----- Step 4: sort the methods, most points first -----
    ranked_names = sorted(scores, key=scores.get, reverse=True)

    results = []
    for name in ranked_names:
        results.append({
            "method": name,
            "score": scores[name],
            "reasons": reasons[name],
        })
    return results


# =====================================================================
# Quick test: run  "python study_expert.py"  to try the engine
# without the screen.
# =====================================================================
if __name__ == "__main__":
    test_answers = {
        "subject": "Memorization", "exam": "Multiple choice", "level": "Beginner",
        "notes": "My notes are messy", "time_left": "1-2 days", "hours": "Less than 1 hour",
        "best_time": "Night", "style": "Visual", "struggle": "Forgetting quickly",
        "focus": "Under 15 minutes", "phone": "Yes, a lot", "place": "Noisy home",
        "company": "Alone",
    }
    for place_number, result in enumerate(find_methods(test_answers)[:3], start=1):
        print(f"{place_number}. {result['method']} - {result['score']} points")
        for reason in result["reasons"]:
            print("     ", reason)
