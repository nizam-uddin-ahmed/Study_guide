"""
app.py  -  THE SCREEN of the Study Method Finder (Streamlit only)

This file only does 4 things:
    1. Shows the 13 questions
    2. Sends the answers to the expert system (study_expert.py)
    3. Shows the DIAGNOSIS (the student's study problems)
    4. Shows the DECISION (the best 3 study methods) and why

All the rules and knowledge are in study_expert.py.

Run with:   streamlit run app.py
"""
import streamlit as st

from study_expert import (METHODS, OPTIONS, TOTAL_RULES, TOTAL_CONDITIONS,
                          TOTAL_DIAGNOSIS_RULES, make_decision)

st.set_page_config(page_title="Study Method Finder", page_icon="📚")
st.title("📚 Study Method Finder")
st.write(f"Answer 13 quick questions. This expert system (a decision support system) will "
         f"diagnose your study problems, check its {TOTAL_RULES} rules "
         "and recommend how you should study.")

# Small icons and names used when showing the result
SEVERITY_ICON = {"Severe": "🔴", "Moderate": "🟠", "Mild": "🟡", "None": "🟢"}
CONFIDENCE_ICON = {"High": "🟢", "Medium": "🟡", "Low": "🟠"}
FACT_TEXT = {
    "urgent": "Your exam is very close (1-2 days)",
    "short_time": "You have little time left",
    "plenty_of_time": "You have plenty of time left",
    "low_study_hours": "You study less than 1 hour per day",
    "attention_risk": "Your attention is at risk (short focus, phone or noise)",
    "weak_materials": "Your study materials are weak (messy notes or only a textbook)",
}


# =====================================================================
# PART 1: THE QUESTIONS
# Each question is (answer name, question text). The answer choices come
# from OPTIONS in study_expert.py.
# =====================================================================
QUESTIONS = [
    ("About your subject", [
        ("subject", "1. What kind of subject are you studying?"),
        ("exam", "2. What kind of exam will you have?"),
        ("level", "3. How well do you know this subject right now?"),
        ("notes", "4. What do your study materials look like?"),
    ]),
    ("About your time", [
        ("time_left", "5. How much time until your exam or deadline?"),
        ("hours", "6. How many hours can you study per day?"),
        ("best_time", "7. When do you have the most energy?"),
    ]),
    ("About you", [
        ("style", "8. How do you learn best?"),
        ("struggle", "9. What is your biggest struggle?"),
        ("focus", "10. How long can you concentrate without a break?"),
        ("phone", "11. Does your phone distract you while studying?"),
        ("place", "12. Where do you usually study?"),
        ("company", "13. Do you prefer to study..."),
    ]),
]

answers = {}    # all the user's answers are collected here

with st.form("questions"):
    for heading, questions in QUESTIONS:
        st.subheader(heading)
        for name, text in questions:
            answers[name] = st.selectbox(text, OPTIONS[name])
    submitted = st.form_submit_button("Find my study methods", type="primary")


# =====================================================================
# PART 2: SHOW THE RESULT (runs only after the user clicks the button)
# =====================================================================
def show_summary(outcome):
    """Decision support: the summary line, the best method and how sure we are."""
    st.header("Decision summary")
    st.info(outcome["summary"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Best method", outcome["decision"]["method"])
    col2.metric("Confidence", f"{CONFIDENCE_ICON[outcome['confidence']]} {outcome['confidence']}")
    col3.metric("Rules matched", f"{outcome['rules_fired']} of {TOTAL_RULES}")


def show_diagnosis(outcome):
    """Diagnosis: the study problems, their cause, symptoms and treatment."""
    st.header("🩺 Diagnosis: your study problems")
    st.caption(f"The system checked {TOTAL_DIAGNOSIS_RULES} diagnosis rules. "
               "Your answers are the symptoms, the study methods are the treatment.")
    for item in outcome["diagnosis"]:
        st.subheader(f"{SEVERITY_ICON[item['severity']]} {item['problem']} ({item['severity']})")
        st.write(f"**Likely cause:** {item['cause']}")
        if item["symptoms"]:
            st.write("**Symptoms found:**")
            for symptom in item["symptoms"]:
                st.write("• " + symptom)
        if item["treatment"]:
            st.write("**Suggested treatment:** " + ", ".join(item["treatment"]))


def show_inferred_facts(outcome):
    """Inferencing: facts the system worked out by itself."""
    with st.expander("🔎 Facts the system inferred from your answers"):
        st.write("You did not type these. The system worked them out from your answers.")
        true_facts = [FACT_TEXT[name] for name, value in outcome["facts"].items() if value]
        if true_facts:
            for text in true_facts:
                st.write("• " + text)
        else:
            st.write("No special facts were inferred.")


def show_top_methods(outcome):
    """Decision making: the 3 best methods, how to do them and why."""
    results = outcome["ranking"]
    best_score = results[0]["score"]     # used to draw the progress bars

    st.header("Your top 3 study methods")
    for number, result in enumerate(results[:3], start=1):
        name = result["method"]
        st.subheader(f"{number}. {name}")
        st.progress(result["score"] / best_score, text=f"Total points: {result['score']}")
        st.write(METHODS[name]["info"])

        with st.expander("How to do it"):
            for step_number, step in enumerate(METHODS[name]["steps"], start=1):
                st.write(f"**{step_number}.** {step}")

        with st.expander("Why was this recommended?"):
            for reason in result["reasons"]:
                st.write("• " + reason)

    other_names = [result["method"] for result in results[3:8]]
    if other_names:
        st.write("**Also worth trying:** " + ", ".join(other_names))
    st.caption("This is advice to support your decision. You choose what to follow.")


if submitted:
    outcome = make_decision(answers)     # runs the whole expert system
    st.divider()

    if outcome["decision"] is None:
        st.warning(outcome["summary"])
    else:
        show_summary(outcome)
        show_diagnosis(outcome)
        show_inferred_facts(outcome)
        show_top_methods(outcome)


# =====================================================================
# PART 3: A SHORT EXPLANATION OF HOW THE SYSTEM WORKS
# =====================================================================
st.divider()
with st.expander("ℹ️ How does this expert system work?"):
    st.write(
        f"""
**Facts:** your 13 answers.

**Inferencing:** the system works out new facts from your answers.
For example: *IF your exam is in 1-2 days, THEN the situation is urgent.*

**Diagnosis:** the system looks at your symptoms and finds your study problems
using **{TOTAL_DIAGNOSIS_RULES} diagnosis rules**. For example: *phone distraction + short focus
= attention problem.* More symptoms means a more severe problem.

**Rules:** the system has **{TOTAL_RULES} IF-THEN rules** with **{TOTAL_CONDITIONS} conditions** in total.
For example: *IF your subject is Memorization, THEN recommend Active Recall (+3 points).*

**Decision making:** every rule that is true adds points to a study method.
The methods with the most points are chosen as the best advice.

**Decision support:** the system does not only give an answer. It also shows the diagnosis,
the reasons, the rules that matched and a confidence level, so you can judge the advice
and make the final choice yourself.
"""
    )
