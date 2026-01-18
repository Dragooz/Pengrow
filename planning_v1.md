1. Goal is to create an appraisal system.
2. 1 Company > many users > each user with 1 role. 
3. 1 user can be appraised by several users, depends on the roles relationship. 
4. Process of appraisal:
    - User itself, can be the one either to be appraised, or to appraise n users.
    - The appraisal form structure roughly:
        - Administrative Data
            - Appraisee's Details section - Name, Position, Division, Date Joined, Last Promotion Date
            - Reviewer's Details: Name, Position, 
            - Date of Discuission Session
            - Period Rated (From and To)
        - Scaling (Exceptional OR Good OR As expected OR weak OR Not Observed)
            - Performance Against Competency Areas
                - Work Efficiency, E.g. 
                    - Ability to work without supervision
                    - Knowledge of roles and responsibilities given,
                    - Work accuracy and correctness
                    - Resourcefulness and creativity
                    - etc...
                - Provide other comments on the individual's work ability and cite specific instances. 

            - Productivity, Administrative and Supervisory
                - Completes tasks according to instructions
                - Takes responsibilty for work
                - Sustain productive work
                - Meets reasonable time estimates
                - etc...
                - Provide other comments on the individual's work ability and suppervisory ability and specifeic instance.

            - Personal
                - Initiative and ambition
                - Manner and appearance.
                - etc.

        - Overall evaluation
            - Poor OR Below Expectative OR Satisfactory OR Above Exceptions OR Excellent
            - Do you feel this person is ready for more advanced work?
            - Ready to be promoted to higher level? 
            - Summary Comment
        
        Signature (Free hand)
            - Signature by Appraisee
            - Signature by Reviewer
            - Signature by PIC (HR)

Tech stack:
1. Django to serve as Backend, Postgres DB, React as Frontend.