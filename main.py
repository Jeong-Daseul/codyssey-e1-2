import json
from datetime import datetime

class Quiz:
      def __init__(self, question, choices, answer):
          if len(choices) != 4:
              raise ValueError("선택지는 4개여야 합니다.")

          if answer < 1 or answer > 4:
              raise ValueError("정답 번호는 1~4여야 합니다.")

          self.question = question
          self.choices = choices
          self.answer = answer

      def display(self):
          print(self.question)

          for index, choice in enumerate(self.choices, start=1):
              print(f"{index}. {choice}")

      def is_correct(self, user_answer):
          return user_answer == self.answer

      def to_dict(self):
          return {
              "question": self.question,
              "choices": self.choices,
              "answer": self.answer
          }

      @classmethod
      def from_dict(cls, data):
          return cls(
              data["question"],
              data["choices"],
              data["answer"]
          )
class QuizGame:
      def __init__(self):
          self.quizzes = []
          self.best_score = 0
          self.history = []

      def add_quiz(self, quiz):
          self.quizzes.append(quiz)

      def list_quizzes(self):
          if not self.quizzes:
              print("등록된 퀴즈가 없습니다.")
              return

          print(f"등록된 퀴즈 목록 ({len(self.quizzes)}개)")

          for index, quiz in enumerate(self.quizzes, start=1):
              print(f"{index}. {quiz.question}")

      def get_quiz_count(self):
          return len(self.quizzes)

      def load_default_quizzes(self):
          default_data = [
              {
                  "question": "Python의 출력 함수는?",
                  "choices": ["input", "print", "open", "read"],
                  "answer": 2
              },
              {
                  "question": "Docker 이미지를 만드는 명령은?",
                  "choices": [
				"docker run",
				"docker build",
				"docker start",
				"docker pull"
				],
                  "answer": 2
              },
              {
                  "question": "Git에서 변경사항을 커밋하는 명령은?",
                  "choices": ["git add", "git commit", "git push", "git clone"],
                  "answer": 2
              },
              {
                  "question": "Python 파일의 일반적인 확장자는?",
                  "choices": [".java", ".js", ".py", ".html"],
                  "answer": 3
              },
              {
                  "question": "Docker 컨테이너 목록을 확인하는 명령은?",
                  "choices": ["docker ps", "docker image", "docker make", "docker list"],
                  "answer": 1
              }
          ]

          self.quizzes = [
              Quiz.from_dict(data)
              for data in default_data
          ]

      def play_quiz(self):
          if not self.quizzes:
              print("등록된 퀴즈가 없습니다.")
              return 0

          score = 0

          print(f"퀴즈를 시작합니다! 총 {len(self.quizzes)}문제입니다.")

          for index, quiz in enumerate(self.quizzes, start=1):
              print()
              print(f"[문제 {index}]")
              quiz.display()

              while True:
                  try:
                      user_answer = int(input("정답 번호: "))

                      if 1 <= user_answer <= 4:
                          break

                      print("1~4 사이의 숫자를 입력하세요.")
                  except ValueError:
                      print("숫자만 입력하세요.")

              if quiz.is_correct(user_answer):
                  print("정답입니다!")
                  score += 1
              else:
                  print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

          percentage = score / len(self.quizzes) * 100
          print()
          print(
              f"결과: {len(self.quizzes)}문제 중 "
              f"{score}문제 정답 ({percentage:.0f}점)"
          )

          if percentage > self.best_score:
              self.best_score = percentage
              print("새로운 최고 점수입니다!")

          self.history.append({
              "played_at": datetime.now().isoformat(timespec="seconds"),
              "total_questions": len(self.quizzes),
              "correct_answers": score,
              "score": percentage
          })

          return score

      def save_state(self, filename="state.json"):
          data = {
              "quizzes": [
                  quiz.to_dict()
                  for quiz in self.quizzes
              ],
              "best_score": self.best_score,
              "history": self.history
          }

          with open(filename, "w", encoding="utf-8") as file:
              json.dump(data, file, ensure_ascii=False, indent=4)

          print("게임 데이터를 저장했습니다.")

      def load_state(self, filename="state.json"):
          try:
              with open(filename, "r", encoding="utf-8") as file:
                  data = json.load(file)

              self.quizzes = [
                  Quiz.from_dict(item)
                  for item in data.get("quizzes", [])
              ]
              self.best_score = data.get("best_score", 0)
              self.history = data.get("history", [])

              print("저장된 게임 데이터를 불러왔습니다.")

          except FileNotFoundError:
              print("저장 파일이 없어 기본 퀴즈를 사용합니다.")
              self.load_default_quizzes()

          except json.JSONDecodeError:
              print("state.json 파일이 손상되어 기본 퀴즈를 사용합니다.")
              self.load_default_quizzes()

      def add_quiz_interactive(self):
          print("새로운 퀴즈를 추가합니다.")
          question = input("문제를 입력하세요: ").strip()

          choices = []
          for index in range(1, 5):
              choice = input(f"선택지 {index}: ").strip()
              choices.append(choice)

          while True:
              try:
                  answer = int(input("정답 번호(1~4): "))
                  if 1 <= answer <= 4:
                      break
                  print("1~4 사이의 숫자를 입력하세요.")
              except ValueError:
                  print("숫자만 입력하세요.")

          self.add_quiz(Quiz(question, choices, answer))
          self.save_state()
          print("퀴즈가 추가되었습니다.")

      def show_score(self):
          print(f"최고 점수: {self.best_score:.0f}점")

          if self.history:
              print(f"게임 기록: {len(self.history)}회")
              latest = self.history[-1]
              print(
                  f"최근 기록: {latest['correct_answers']}/"
                  f"{latest['total_questions']}문제, "
                  f"{latest['score']:.0f}점"
              )
          else:
              print("게임 기록이 없습니다.")

      def delete_quiz_interactive(self):
          if not self.quizzes:
              print("삭제할 퀴즈가 없습니다.")
              return

          self.list_quizzes()

          while True:
              try:
                  number = int(input("삭제할 퀴즈 번호(취소: 0): "))

                  if number == 0:
                      print("삭제를 취소했습니다.")
                      return

                  if 1 <= number <= len(self.quizzes):
                      deleted = self.quizzes.pop(number - 1)
                      self.save_state()
                      print(f"삭제 완료: {deleted.question}")
                      return

                  print("목록에 있는 번호를 입력하세요.")
              except ValueError:
                  print("숫자만 입력하세요.")

      def run(self):
          self.load_state()

          while True:
              print()
              print("=" * 40)
              print("Python·Docker·Git 퀴즈 게임")
              print("1. 퀴즈 풀기")
              print("2. 퀴즈 추가")
              print("3. 퀴즈 목록")
              print("4. 점수 확인")
              print("5. 퀴즈 삭제")
              print("6. 종료")
              print("=" * 40)

              choice = input("메뉴를 선택하세요: ").strip()

              if choice == "1":
                  self.play_quiz()
                  self.save_state()
              elif choice == "2":
                  self.add_quiz_interactive()
              elif choice == "3":
                  self.list_quizzes()
              elif choice == "4":
                  self.show_score()
              elif choice == "5":
                  self.delete_quiz_interactive()
              elif choice == "6":
                  self.save_state()
                  print("게임을 종료합니다.")
                  break
              else:
                  print("1~6 사이의 메뉴를 선택하세요.")


if __name__ == "__main__":
    game = QuizGame()
    game.run()
