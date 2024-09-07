# Edullam - Tomar & Kids

This project is a Django-based backend for generating roadmaps, multiple-choice questions (MCQs), and interview questions, as well as scoring answers using AI models.

## Project Structure

```
.env
.gitignore
db.sqlite3
diversity_backend/
	__init__.py
	__pycache__/
	asgi.py
	settings.py
	urls.py
	wsgi.py
generate_roadmap/
	__init__.py
	__pycache__/
	admin.py
	ai/
		hello.txt
		main.py
		quiz_data.py
		requirements.txt
		similar_neighbours.py
	apps.py
	fetch_courses.py
	migrations/
		__init__.py
		__pycache__/
	models.py
	qna.json
	serializers.py
	testing.ipynb
	tests.py
	urls.py
	views.py
manage.py
requirements.txt
roadmap_output.txt
test.py
```

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   - Create a [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/.env") file in the root directory.
   - Add the necessary environment variables, such as [`GENERATIVE_API_KEY`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fai%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A35%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition").

5. Apply database migrations:

   ```sh
   python manage.py migrate
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

### Endpoints

- **Generate Roadmap**: [`GET /generate-roadmap/`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A55%2C%22character%22%3A20%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition")

  - Parameters: [`skill`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A55%2C%22character%22%3A4%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition"), [`current_skill_level`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A56%2C%22character%22%3A4%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition"), [`target_skill_level`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A57%2C%22character%22%3A4%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition"), [`price`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A58%2C%22character%22%3A4%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition")
  - Example: `/generate-roadmap/?skill=Python&current_skill_level=beginner&target_skill_level=expert&price=free`

- **Generate MCQs**: [`GET /generate-mcqs/`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A55%2C%22character%22%3A20%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition")

- **Generate Interview Questions**: [`GET /generate-interview-questions/`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A55%2C%22character%22%3A20%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition")

- **Score Answers**: `POST /score/`
  - Upload a JSON file containing questions and answers.

### Example JSON for Scoring Answers

```json
{
  "questions_and_answers": [
    {
      "question": "What is Python?",
      "answer": "Python is a programming language."
    }
  ]
}
```

## Code Overview

### Main Modules

- **[`diversity_backend/urls.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fdiversity_backend%2Furls.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/diversity_backend/urls.py")**: Configures the URL routing for the project.
- **[`generate_roadmap/urls.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Furls.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/urls.py")**: Defines the URL patterns for the [`generate_roadmap`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap") app.
- **[`generate_roadmap/views.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/views.py")**: Contains view functions for handling requests.
  - [`score_answers`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22score_answers%22%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/views.py"): Handles scoring of answers.
  - [`generate_roadmap`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22generate_roadmap%22%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/views.py"): Generates a learning roadmap.
- **[`generate_roadmap/ai/main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fai%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/ai/main.py")**: Contains AI-related functions.
  - [`ai_main`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fai%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22ai_main%22%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "/mnt/d/Work/Development/sih_2024/diversity_backend/generate_roadmap/ai/main.py"): Main function for processing questions and generating answers.

### AI Integration

- Uses Google Generative AI ([`gemini-1.5-flash`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fai%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A0%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition")) for generating content.
- Utilizes [`langchain`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fmnt%2Fd%2FWork%2FDevelopment%2Fsih_2024%2Fdiversity_backend%2Fgenerate_roadmap%2Fai%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A5%7D%7D%5D%2C%22449b6aae-1768-419b-9f2b-02c41e72375a%22%5D "Go to definition") for text processing and similarity scoring.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries, please contact [at927@snu.edu.in].
