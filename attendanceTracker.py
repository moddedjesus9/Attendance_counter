from os import remove
from sys import exit


enrollID = {
    "BCA": [
        "2421100000",
        "2421100001",
        "2421100002",
        "2421100003",
        "2421100004",
        "2421100005",
        "2421100006",
        "2421100007",
        "2421100008",
        "2421100009",
        "2421100010",
        "2421100011",
        "2421100012",
        "2421100013",
        "2421100014",
        "2421100015",
        "2421100016",
        "2421100017",
        "2421100018",
        "2421100019",
        "2421100020",
        "2421100021",
        "2421100022",
        "2421100023",
        "2421100024",
        "2421100025",
        "2421100026",
        "2421100027",
        "2421100028",
        "2421100029",
    ],
    "BSC": [
        "2421100554",
        "2421100620",
        "2421100635",
        "2421100644",
        "2421100667",
        "2421100718",
        "2421100720",
        "2421100731",
        "2421100735",
        "2421100757",
        "2421100762",
        "2421100767",
        "2421100806",
        "2421100834",
        "2421100845",
        "2421100910",
        "2421100911",
        "2421100929",
        "2421100941",
        "2421100960",
    ],
}


def extractAttendance(fileAddress):
    try:
        with open(fileAddress + ".txt", encoding="utf-8") as f:
            with open("attendance.txt", "w") as a:
                lines = f.readlines()
                total = len(lines)
                i = 0
                while i < total:
                    if (
                        (
                            lines[i][:-1].upper().strip().endswith("BCA")
                            or lines[i][:-1].upper().strip().endswith("CSC")
                            or lines[i][:-1].upper().strip().endswith("BSC")
                        )
                        and lines[i + 1].capitalize().strip().startswith("Date")
                        and lines[i + 2].capitalize().strip().startswith("Present")
                    ):
                        lines[i] = lines[i].upper().strip()[-3:].replace("CSC", "BSC")
                        lines[i + 1] = (
                            lines[i + 1]
                            .replace("-", ".")
                            .replace("/", ".")
                            .strip()
                            .rstrip("26")
                            .rstrip("20")
                            + "2026"
                        )
                        lines[i + 1] = "Date: " + lines[i + 1][-10:]
                        lines[i + 2] = lines[i + 2].capitalize().strip()
                        a.write(
                            lines[i] + "\n" + lines[i + 1] + "\n" + lines[i + 2] + "\n"
                        )
                        i += 3
                    else:
                        i += 1
                        continue

                    j = i
                    while j < total:
                        lines[j] = (
                            lines[j].rstrip(" <This message was edited>\n") + "\n"
                        )
                        if not (lines[j][-11:-1].isdigit()):
                            a.write("\n")
                            break

                        a.write(lines[j][-11:])
                        j += 1

                    i += 1
    except FileNotFoundError:
        print("\nFile not found!\n")
        ch = input("Press ENTER to proceed...\n\n")
        if ch == "":
            main()


def checkAttendance(roll):
    if roll in enrollID["BCA"] or roll in enrollID["BSC"]:
        with open("attendance.txt") as f:
            content = f.read()
            f.seek(0)
            linesList = f.readlines()
        attended = content.count(roll)
        days = set()
        for line in linesList:
            if line.startswith("Date"):
                days.add(line[-11:-1])
        totalDays = len(days)
        print(
            f"\nStudent with enrollment no. {roll} has attended {attended} out of {totalDays} classes.\nTotal Attendance: {round(((attended/totalDays)*100), 2)} %\n"
        )
    else:
        print("Enrollment ID not found!\n")
    ch = input("Press ENTER to proceed...\n\n")
    if ch == "":
        queries()


def viewAttendance(course):
    if course.lower() not in ["bca", "bsc"]:
        print("Course not found!\n")
        ch = input("Press ENTER to proceed...\n\n")
        if ch == "":
            queries()

    print(f"\nATTENDANCE REPORT\nCourse: {course.upper()}")
    with open("attendance.txt") as f:
        content = f.read()
        f.seek(0)
        linesList = f.readlines()
    days = set()
    for line in linesList:
        if line.startswith("Date"):
            days.add(line[-11:-1])
    totalDays = len(days)
    print(
        f"Total number of students enrolled in {course.upper()}: {len(enrollID[course.upper()])}"
    )
    print(f"Total number of classes conducted: {totalDays}\n")
    print(f"ENROLLMENT NO.\t\tNO. OF CLASSES ATTENDED\t\tTOTAL ATTENDANCE\n{'-'*72}")
    for roll in enrollID[course.upper()]:
        print(
            f"{roll}\t\t{content.count(roll)}\t\t\t\t{round((content.count(roll)/totalDays)*100, 2)} %"
        )
    print()
    ch = input("Press ENTER to proceed...\n\n")
    if ch == "":
        queries()


def queries():
    print(
        "SELECT OPERATION TO PROCEED:\n\t1. Check total attendance of individual student\n\t2. View total attendance of all students\n\t3. Exit"
    )
    choice = input("\nEnter choice: ")
    if choice == "1":
        roll = input("\nEnter enrollment no. of student: ")
        checkAttendance(roll)
    elif choice == "2":
        course = input("Enter course (BCA/BSC): ")
        viewAttendance(course)
    elif choice == "3":
        print()
        remove("attendance.txt")
        exit()
    else:
        print("\nInvalid input!\n")
        ch = input("Press ENTER to proceed...\n\n")
        if ch == "":
            queries()


def main():
    fileAddress = input("\nEnter file address of exported chat along with file name: ")
    extractAttendance(fileAddress)
    print("\nAttendance records extracted successfully!\n")
    queries()


main()
