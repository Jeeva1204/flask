from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

# File to store data
DATA_FILE = 'students.txt'

def read_students():
    """Read all students from the file"""
    students = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            for line in file:
                if line.strip():
                    id, name, class_name, subject, marks = line.strip().split(',')
                    students.append({
                        'id': id,
                        'name': name,
                        'class': class_name,
                        'subject': subject,
                        'marks': marks
                    })
    return students

def write_students(students):
    """Write all students to the file"""
    with open(DATA_FILE, 'w') as file:
        for student in students:
            file.write(f"{student['id']},{student['name']},{student['class']},{student['subject']},{student['marks']}\n")

@app.route('/')
def index():
    """Display all students"""
    students = read_students()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        students = read_students()
        new_id = str(len(students) + 1)
        
        new_student = {
            'id': new_id,
            'name': request.form['name'],
            'class': request.form['class'],
            'subject': request.form['subject'],
            'marks': request.form['marks']
        }
        
        students.append(new_student)
        write_students(students)
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    """Edit an existing student"""
    students = read_students()
    student = next((s for s in students if s['id'] == id), None)
    
    if student is None:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['class'] = request.form['class']
        student['subject'] = request.form['subject']
        student['marks'] = request.form['marks']
        
        write_students(students)
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', student=student)

@app.route('/delete/<id>')
def delete_student(id):
    """Delete a student"""
    students = read_students()
    students = [s for s in students if s['id'] != id]
    write_students(students)
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 