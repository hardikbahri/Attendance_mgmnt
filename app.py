import eel

import login_page
import attendance
import report_generation
import leave

eel.init('web')



# Login function
eel.expose(login_page.login)
eel.expose(login_page.register_user)
eel.expose(attendance.attendance_registration)
eel.expose(report_generation.report_generation_se)
eel.expose(leave.request_leave)
eel.expose(leave.check_leave_status)
eel.expose(leave.approve_leave)
eel.expose(leave.emp_rep)
eel.expose(leave.check_leave)

@eel.expose
def open_new_window(page):
    eel.start(page, size=(600, 400), block=False)



if __name__ == '__main__':
    eel.start('index.html', size=(600, 400))
    
