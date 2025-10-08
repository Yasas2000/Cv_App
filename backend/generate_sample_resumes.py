"""
Script to generate sample PDF resumes for testing
Requires: reportlab library
Run: pip install reportlab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import os

def create_resume(filename, data):
    """Create a PDF resume with given data"""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=8,
        spaceBefore=12
    )
    
    # Name
    name = Paragraph(data['name'], title_style)
    story.append(name)
    
    # Contact info
    contact = Paragraph(
        f"{data['email']} | {data['phone']} | {data['location']}",
        styles['Normal']
    )
    story.append(contact)
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    if 'summary' in data:
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(data['summary'], styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_text = " • ".join(data['skills'])
    story.append(Paragraph(skills_text, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    # Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    for exp in data['experience']:
        job_title = Paragraph(
            f"<b>{exp['title']}</b> - {exp['company']}<br/>{exp['duration']}",
            styles['Normal']
        )
        story.append(job_title)
        
        for achievement in exp['achievements']:
            bullet = Paragraph(f"• {achievement}", styles['Normal'])
            story.append(bullet)
        
        story.append(Spacer(1, 0.1*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    for edu in data['education']:
        edu_text = Paragraph(
            f"<b>{edu['degree']}</b> - {edu['school']}<br/>{edu['year']}",
            styles['Normal']
        )
        story.append(edu_text)
        story.append(Spacer(1, 0.05*inch))
    
    doc.build(story)
    print(f"Created: {filename}")

# Sample resume data
resumes_data = [
    {
        'filename': 'Sarah_Johnson_Senior_React_Developer.pdf',
        'name': 'Sarah Johnson',
        'email': 'sarah.johnson@email.com',
        'phone': '555-123-4567',
        'location': 'San Francisco, CA',
        'summary': '6+ years of experience building scalable web applications using React and Node.js. Specialized in fintech and e-commerce platforms with a strong focus on performance optimization and user experience.',
        'skills': [
            'React', 'Node.js', 'JavaScript', 'TypeScript', 'Redux', 'Next.js',
            'AWS', 'Docker', 'GraphQL', 'REST API', 'MongoDB', 'PostgreSQL',
            'Git', 'Agile', 'Jest', 'Webpack'
        ],
        'experience': [
            {
                'title': 'Senior Frontend Developer',
                'company': 'FinTech Solutions Inc.',
                'duration': 'Jan 2021 - Present (3 years)',
                'achievements': [
                    'Led development of real-time trading platform using React and WebSockets, serving 100K+ daily users',
                    'Improved application performance by 40% through code splitting and lazy loading',
                    'Mentored team of 4 junior developers and conducted code reviews'
                ]
            },
            {
                'title': 'Full Stack Developer',
                'company': 'E-Commerce Corp',
                'duration': 'Jun 2018 - Dec 2020 (2.5 years)',
                'achievements': [
                    'Built microservices architecture using Node.js and Express for payment processing',
                    'Developed responsive React components for product catalog with 10M+ products',
                    'Integrated third-party APIs including Stripe, PayPal, and shipping providers'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'school': 'University of California, Berkeley',
                'year': '2018'
            }
        ]
    },
    {
        'filename': 'Michael_Chen_Full_Stack_Engineer.pdf',
        'name': 'Michael Chen',
        'email': 'michael.chen@email.com',
        'phone': '555-234-5678',
        'location': 'New York, NY',
        'summary': '5 years of full-stack development experience with expertise in Python, Django, and React. Proven track record in healthcare and SaaS applications with focus on security and scalability.',
        'skills': [
            'Python', 'Django', 'React', 'PostgreSQL', 'Docker', 'Kubernetes',
            'AWS', 'Redis', 'Celery', 'REST API', 'Git', 'CI/CD',
            'Linux', 'Nginx', 'GraphQL', 'TypeScript'
        ],
        'experience': [
            {
                'title': 'Full Stack Engineer',
                'company': 'HealthTech Systems',
                'duration': 'Mar 2020 - Present (4 years)',
                'achievements': [
                    'Developed HIPAA-compliant patient management system using Django and React',
                    'Implemented secure authentication system with 2FA and role-based access control',
                    'Reduced API response time by 60% through database optimization and caching strategies'
                ]
            },
            {
                'title': 'Backend Developer',
                'company': 'SaaS Startup Co.',
                'duration': 'Jul 2019 - Feb 2020 (8 months)',
                'achievements': [
                    'Built RESTful APIs using Django REST Framework serving 50K+ requests/day',
                    'Containerized applications using Docker and deployed to AWS ECS',
                    'Implemented automated testing achieving 85% code coverage'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Master of Science in Software Engineering',
                'school': 'Columbia University',
                'year': '2019'
            }
        ]
    },
    {
        'filename': 'Emily_Rodriguez_Data_Scientist.pdf',
        'name': 'Emily Rodriguez',
        'email': 'emily.rodriguez@email.com',
        'phone': '555-345-6789',
        'location': 'Austin, TX',
        'summary': '4 years of experience in data science and machine learning with focus on fintech and analytics. Expert in building predictive models and deploying ML solutions to production.',
        'skills': [
            'Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'scikit-learn',
            'SQL', 'Pandas', 'NumPy', 'Deep Learning', 'NLP', 'Computer Vision',
            'AWS', 'Docker', 'Git', 'Jupyter', 'MLflow', 'Airflow'
        ],
        'experience': [
            {
                'title': 'Senior Data Scientist',
                'company': 'Financial Analytics Group',
                'duration': 'May 2021 - Present (3 years)',
                'achievements': [
                    'Developed fraud detection model using ensemble methods with 95% accuracy',
                    'Built credit risk assessment system processing 100K+ applications monthly',
                    'Deployed ML models to production using Docker and AWS SageMaker'
                ]
            },
            {
                'title': 'Data Scientist',
                'company': 'Tech Analytics Inc.',
                'duration': 'Aug 2020 - Apr 2021 (9 months)',
                'achievements': [
                    'Created customer churn prediction model improving retention by 25%',
                    'Implemented recommendation engine using collaborative filtering',
                    'Automated data pipeline using Python and Apache Airflow'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Master of Science in Data Science',
                'school': 'University of Texas at Austin',
                'year': '2020'
            }
        ]
    },
    {
        'filename': 'David_Kim_Backend_Developer.pdf',
        'name': 'David Kim',
        'email': 'david.kim@email.com',
        'phone': '555-456-7890',
        'location': 'Seattle, WA',
        'summary': '7 years of backend development experience specializing in Java, Spring Boot, and microservices architecture. Expert in building scalable enterprise applications and cloud-native solutions.',
        'skills': [
            'Java', 'Spring Boot', 'Kubernetes', 'Microservices', 'MongoDB',
            'PostgreSQL', 'Redis', 'Kafka', 'Docker', 'AWS', 'Azure',
            'REST API', 'GraphQL', 'Jenkins', 'Git', 'Maven'
        ],
        'experience': [
            {
                'title': 'Senior Backend Engineer',
                'company': 'Enterprise Cloud Solutions',
                'duration': 'Jan 2019 - Present (5 years)',
                'achievements': [
                    'Architected microservices platform using Spring Boot and Kubernetes serving 1M+ users',
                    'Implemented event-driven architecture using Apache Kafka for real-time data processing',
                    'Reduced infrastructure costs by 35% through cloud optimization and auto-scaling'
                ]
            },
            {
                'title': 'Java Developer',
                'company': 'Corporate Systems Ltd.',
                'duration': 'Jun 2017 - Dec 2018 (1.5 years)',
                'achievements': [
                    'Developed RESTful APIs using Spring Boot and Spring Data JPA',
                    'Migrated monolithic application to microservices architecture',
                    'Implemented CI/CD pipeline using Jenkins and Docker'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Engineering in Computer Science',
                'school': 'University of Washington',
                'year': '2017'
            }
        ]
    },
    {
        'filename': 'Jessica_Williams_Frontend_Engineer.pdf',
        'name': 'Jessica Williams',
        'email': 'jessica.williams@email.com',
        'phone': '555-567-8901',
        'location': 'Los Angeles, CA',
        'summary': '3 years of frontend development experience with passion for creating beautiful, user-friendly interfaces. Specialized in React, Vue.js, and modern web technologies.',
        'skills': [
            'React', 'Vue.js', 'JavaScript', 'TypeScript', 'HTML5', 'CSS3',
            'Sass', 'Tailwind CSS', 'Webpack', 'Vite', 'Jest', 'Cypress',
            'Git', 'Figma', 'Responsive Design', 'UI/UX'
        ],
        'experience': [
            {
                'title': 'Frontend Engineer',
                'company': 'Startup Innovations',
                'duration': 'Sep 2021 - Present (2.5 years)',
                'achievements': [
                    'Built consumer-facing mobile app using React Native reaching 500K+ downloads',
                    'Implemented design system with reusable components used across 5 products',
                    'Improved website performance score from 65 to 95 using Lighthouse optimization techniques'
                ]
            },
            {
                'title': 'Junior Frontend Developer',
                'company': 'Digital Agency Co.',
                'duration': 'Jul 2021 - Aug 2021 (1 year)',
                'achievements': [
                    'Developed responsive websites using Vue.js and Tailwind CSS for 10+ clients',
                    'Collaborated with designers to implement pixel-perfect UI components',
                    'Optimized bundle size reducing load time by 50%'
                ]
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Arts in Web Development',
                'school': 'UCLA Extension',
                'year': '2021'
            }
        ]
    }
]

def main():
    # Create resumes directory if it doesn't exist
    resumes_dir = os.path.join(os.path.dirname(__file__), '..', 'resumes')
    os.makedirs(resumes_dir, exist_ok=True)
    
    print("Generating sample PDF resumes...")
    print("-" * 50)
    
    for resume_data in resumes_data:
        filename = os.path.join(resumes_dir, resume_data['filename'])
        create_resume(filename, resume_data)
    
    print("-" * 50)
    print(f"✓ Successfully generated {len(resumes_data)} sample resumes!")
    print(f"✓ Resumes saved to: {resumes_dir}")

if __name__ == '__main__':
    main()
