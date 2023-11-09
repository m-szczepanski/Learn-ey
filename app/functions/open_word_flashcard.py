from app.components.words_learning import WordFlashcard


def open_word_flashcard(language):
    app = WordFlashcard(language)
    app.mainloop()
