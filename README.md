# "Project Koh"

SE 329, Project 1

![Koh the Face Stealer](Koh.png)

## Goal

We will create an application that helps a professor identify
the students in a classroom. The application will use a camera
and facial recognition to scan students individually and display
the name and picture of each student to the professor as it
recognizes them. If the application sees a student who hasn’t
been identified, it gives the professor the opportunity to
enter the student’s name so he or she will be identified in the
future.

## Discussion

Project Koh will be a cloud based software system that houses
the server. A cloud application model allows for multiple
front-end applications to interact with the server across
multiple devices. This would provide professors many options to
learn more about their students. However, the first versions will
only be compatible with laptop computers with a camera.

Project Koh is what Iowa State University needs to create personal
relationships between faculty and students. When this relationship
is formed, students are more likely to attend class. ISU can
expect to see an increase students, who graduate in four years or
less; decrease in dropped classes; and an increase of students
hired within six months after graduation. These reported
statistics will align with university trends that students who
attend class on a regular basis have higher Grade Point Averages
(GPA) than those who don’t.

The university can look to extend Project Koh’s applications to
giving teaching assistants access to the application for
recitations, as well as Supplemental Instruction leaders to lead
their sessions. We want to encourage strong relationships to
expand Iowa State’s continuous learning environment.

## Other Thoughts

Beyond the MVP, our stretch goal is to deliver an extended product
that has all the functionality of the MVP, as well as some or all
of the following:

- A fully featured UI.
- Increased integration, providing the ability to take a picture
  from the UI directly.
- Multi-face recognition in a single photo (possibly from a video
  stream)
- Maintainable class roster.
- Multi-platform support.

Multi-platform operability would be possible by structuring the
server in a generic way. Any user only needs to send an image to
the server and it responds with information. Structuring the
server this way provides the freedom to develop the client-side
software independently.

Continuous video stream inspection would allow the interface to
be hands free. Rather than having to click to take a photo and
send it to the server, the whole process is automatic. The
camera is continuously running and each frame is checked to see
if it contains a face. If so, identity information is displayed.

An example of a combination of these stretch goals could be
implemented on the Microsoft Hololens. If an instructor is
wearing a Hololens while instructing, the device could
continuously be scanning the recognizable faces in the audience
and adding a name icon above them in real time using augmented
reality. If a professor wants to call on a student, they would
have their name available to them.

An example of the class roster function would allow the professor
to go about lecture as he or she normally would while the system
automatically takes attendance. If there are any unknown
students or absent students, it would ask the professor to
confirm whether the student was present or not. An extension of
this idea could be a professor logging in and selecting which
class he is teaching and a corresponding roster being loaded.
If any students are unrecognized or incorrectly identified, the
professor could select them from the list to help retrain the
server.

For more information regarding the title of this project, [click
here](http://avatar.wikia.com/wiki/Koh).

## Creators

International Justice League of Super Acquaintances

- Brody Concannon
- Nathan Karasch
- Stefan Kraus
- Gregory Steenhagen

![International Justice League of Super Acquaintances](IJLSA.jpg)

# Frameworks
    - Socket IO - Javascript socket framework.
        - To use, first install nodeJS
        - Then run
            ```
            npm install socket.io
            ```

