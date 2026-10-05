from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = {
    "S001":{"name": "Ravi", "marks": 85, "grade": "A"},
    "S002":{"name": "Kishan", "marks": 72, "grade": "A"},
    "S003":{"name": "Pinky", "marks": 91, "grade": "A+"}
}

#input schema for submitting marks
class MarksSubmission(BaseModel):
    student_id: str
    marks: int
    subject: str

@app.get("/students/{student_id}")
def get_students(student_id: str):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {student_id} does not exists"
        )

    return students[student_id]


@app.post("/submit-marks")
def submit_marks(submission: MarksSubmission):
    # error 1 student does not exists
    if submission.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {submission.student_id} does not exists"
        )

    # error 2 marks valid range 0 - 100
    if submission.marks < 0 or submission.marks > 100:
        raise HTTPException(
            status_code=400,
            detail={
                "Error": "Marks must be between 0 and 100",
                "marks_received": submission.marks,
                "Fix": "Enter a valid marks between 0 and 100"
            }
        )


    # error 3 Subject name empty
    if submission.subject.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Subject name cannot be empty"
        )

    try:
        students[submission.student_id]["marks"] = submission.marks

        return{
            "Message": "Marks Submitted Successfully",
            "Student": students[submission.student_id]["name"],
            "Subject": submission.subject,
            "Marks": submission.marks
        }
    
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong on our side: {str(err)}"
        )