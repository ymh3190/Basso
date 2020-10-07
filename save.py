import openpyxl

def save_to_file(jobs):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["title", "company", "location", "link"])
    for job in jobs:
        sheet.append(list(job.values()))
    wb.save("saramin.xlsx")
    return
