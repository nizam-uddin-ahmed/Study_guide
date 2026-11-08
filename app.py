"""
app.py  -  THE SCREEN of the Study Method Finder (Streamlit only)

This file only does 3 things:
    1. Shows the 13 questions
    2. Sends the answers to the expert system (study_expert.py)
    3. Shows the best 3 study methods

All the rules and knowledge are in study_expert.py.

Run with:   streamlit run app.py
"""
import streamlit as st

from study_expert import METHODS, OPTIONS, TOTAL_RULES, TOTAL_CONDITIONS, find_methods

st.set_page_config(page_title="Study Method Finder", page_icon="📚")

st.title("📚 Study Method Finder")
st.write(f"Answer 13 quick questions. The expert system will check its {TOTAL_RULES} rules "
         "and recommend how you should study.")


# =====================================================================
# PART 1: THE QUESTIONS
# Each answer is saved in a variable (subject, exam, level, ...).
# The answer choices come from OPTIONS in study_expert.py.
# =====================================================================
with st.form("questions"):

    st.subheader("About your subject")
    subject = st.selectbox("1. What kind of subject are you studying?", OPTIONS["subject"])
    exam = st.selectbox("2. What kind of exam will you have?", OPTIONS["exam"])
    level = st.selectbox("3. How well do you know this subject right now?", OPTIONS["level"])
    notes = st.selectbox("4. What do your study materials look like?", OPTIONS["notes"])

    st.subheader("About your time")
    time_left = st.selectbox("5. How much time until your exam or deadline?", OPTIONS["time_left"])
    hours = st.selectbox("6. How many hours can you study per day?", OPTIONS["hours"])
    best_time = st.selectbox("7. When do you have the most energy?", OPTIONS["best_time"])

    st.subheader("About you")
    style = st.selectbox("8. How do you learn best?", OPTIONS["style"])
    struggle = st.selectbox("9. What is your biggest struggle?", OPTIONS["struggle"])
    focus = st.selectbox("10. How long can you concentrate without a break?", OPTIONS["focus"])
    phone = st.selectbox("11. Does your phone distract you while studying?", OPTIONS["phone"])
    place = st.selectbox("12. Where do you usually study?", OPTIONS["place"])
    company = st.selectbox("13. Do you prefer to study...", OPTIONS["company"])

    submitted = st.form_submit_button("Find my study methods", type="primary")


# =====================================================================
# PART 2: RUN THE EXPERT SYSTEM AND SHOW THE RESULT
# This part runs only after the user clicks the button.
# =====================================================================
if submitted:

    # Put all answers in one dictionary and give it to the expert system
    answers = {
        "subject": subject,
        "exam": exam,
        "level": level,
        "notes": notes,
        "time_left": time_left,
        "hours": hours,
        "best_time": best_time,
        "style": style,
        "struggle": struggle,
        "focus": focus,
        "phone": phone,
        "place": place,
        "company": company,
    }
    results = find_methods(answers)      # best method is first in the list

    # Count how many rules were true
    rules_fired = 0
    for result in results:
        rules_fired = rules_fired + len(result["reasons"])

    best_score = results[0]["score"]     # used to draw the progress bars

    st.divider()
    st.header("Your top 3 study methods")
    st.caption(f"{rules_fired} of the {TOTAL_RULES} rules matched your answers.")

    # Show the 3 best methods
    top_three = results[:3]
    for place_number, result in enumerate(top_three, start=1):
        name = result["method"]

        st.subheader(f"{place_number}. {name}")
        st.progress(result["score"] / best_score, text=f"Total points: {result['score']}")
        st.write(METHODS[name]["info"])

        with st.expander("How to do it"):
            for step_number, step in enumerate(METHODS[name]["steps"], start=1):
                st.write(f"**{step_number}.** {step}")

        with st.expander("Why was this recommended?"):
            for reason in result["reasons"]:
                st.write("• " + reason)

    # Show the next best methods in one line
    other_methods = results[3:8]
    if len(other_methods) > 0:
        names = []
        for result in other_methods:
            names.append(result["method"])
        st.write("**Also worth trying:** " + ", ".join(names))


# =====================================================================
# PART 3: A SHORT EXPLANATION OF HOW THE SYSTEM WORKS
# =====================================================================
st.divider()
with st.expander("ℹ️ How does this expert system work?"):
    st.write(
        f"""
**Facts:** your 13 answers.

**Rules:** the system has **{TOTAL_RULES} IF-THEN rules** with **{TOTAL_CONDITIONS} conditions** in total.
For example: *IF your subject is Memorization, THEN recommend Active Recall (+3 points).*

**Inference:** every rule that is true adds points to a study method.

**Result:** the methods with the most points are shown first, together with the rules that recommended them.
"""
    )
