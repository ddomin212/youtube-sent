from flask import render_template, redirect, session

def registerController(auth, request):
    if request.method == 'POST':
        # register route for email/password authentication
        # get user input from request body
        email = request.form.get('email')
        password = request.form.get('password')

        # create user account with email and password
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return redirect('/login')
        except:
            return render_template('message.html', error_message="User creation failed", status_code=400), 400
    else:
        return render_template("register.html")
    
def profileController(auth, request):
    if request.method == 'POST':
        # get user input from request body
        name = request.form.get('fullname')
        email = request.form.get('email')
        user = auth.get_user_by_email(session.get('user')['email'])
        try:
            # update user account with email and password
            auth.update_user(user.uid, display_name=name, email=email)
        except Exception as e:
            print(e)
        session['user']['email'] = email
        session['user']['name'] = name
        return render_template('profile.html', user=session['user'])
    else:
        return render_template('profile.html', user=session['user'])