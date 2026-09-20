"""A verified printed page bypasses the legacy chapter-dropdown requirement."""
import pathlib
import unittest


class DirectBookPageStartTests(unittest.TestCase):
    def test_page_picker_starts_with_no_indexed_chapter_selected(self):
        js=pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn('document.addEventListener("click",event=>{',js)
        self.assertIn('event.target?.closest?.("#startLesson")',js)
        self.assertIn('prepareExactPageLesson()',js)
        self.assertIn('option.dataset.nabilPageTemporary="yes"',js)
        self.assertIn('select.value=synthetic',js)
        self.assertIn('body.set("book_page",String(picker.value))',js)
        self.assertIn('if(!/^\\d{1,4}$/.test(raw)',js)

    def test_invalid_page_does_not_create_fake_dropdown_lesson(self):
        js=pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn('if(temporary?.dataset?.nabilPageTemporary==="yes")',js)
        self.assertIn('temporary.remove()',js)
        self.assertIn('Number(raw)<1',js)

    def test_real_title_remains_unmodified_when_selected(self):
        js=pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn('if(existing&&existing!=="المحتوى قيد الفهرسة"',js)


if __name__=="__main__":
    unittest.main()
