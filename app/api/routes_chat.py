function updateLessons() {

    const grade =
        gradeSelect.value;

    const subject =
        subjectSelect.value;

    const language =
        languageSelect.value;

    let lessons = [];
    let usedFallbackLanguage = false;

    const gradeData =
        curriculumIndex?.[subject]?.[grade];

    if (gradeData) {

        // =========================
        // أولاً: اللغة المختارة
        // =========================

        const languageData =
            gradeData[language];

        if (
            Array.isArray(languageData)
        ) {

            lessons =
                [...languageData];

        }

        else if (
            languageData &&
            typeof languageData === "object"
        ) {

            Object.values(
                languageData
            ).forEach(
                value => {

                    if (
                        Array.isArray(value)
                    ) {

                        lessons.push(
                            ...value
                        );

                    }

                }
            );

        }

        // =========================
        // Fallback:
        // إذا لم توجد دروس باللغة المختارة
        // =========================

        if (
            lessons.length === 0
        ) {

            usedFallbackLanguage = true;

            Object.entries(
                gradeData
            ).forEach(
                ([availableLanguage, value]) => {

                    if (
                        Array.isArray(value)
                    ) {

                        value.forEach(
                            lesson => {

                                lessons.push(
                                    `${lesson} [${availableLanguage}]`
                                );

                            }
                        );

                    }

                    else if (
                        value &&
                        typeof value === "object"
                    ) {

                        Object.values(
                            value
                        ).forEach(
                            nested => {

                                if (
                                    Array.isArray(nested)
                                ) {

                                    nested.forEach(
                                        lesson => {

                                            lessons.push(
                                                `${lesson} [${availableLanguage}]`
                                            );

                                        }
                                    );

                                }

                            }
                        );

                    }

                }
            );

        }

    }

    // =========================
    // إزالة التكرار
    // =========================

    lessons = [
        ...new Set(lessons)
    ];

    // =========================
    // إعادة بناء القائمة
    // =========================

    lessonSelect.innerHTML = "";

    const first =
        document.createElement(
            "option"
        );

    first.value = "";

    if (
        lessons.length > 0
    ) {

        first.textContent =
            usedFallbackLanguage
                ? "اختر الدرس - بعض الدروس بلغة أخرى"
                : "اختر الدرس";

    }

    else {

        first.textContent =
            "لا توجد دروس مفهرسة لهذا الاختيار بعد";

    }

    lessonSelect.appendChild(
        first
    );

    lessons.forEach(
        lesson => {

            const option =
                document.createElement(
                    "option"
                );

            option.value =
                lesson;

            option.textContent =
                lesson;

            lessonSelect.appendChild(
                option
            );

        }
    );

    // =========================
    // حالة الفهرسة
    // =========================

    if (
        indexStatus
    ) {

        if (
            lessons.length === 0
        ) {

            indexStatus.textContent =
                "لا توجد دروس مفهرسة بعد لهذا الصف والمادة.";

        }

        else if (
            usedFallbackLanguage
        ) {

            indexStatus.textContent =
                "لم نجد دروسًا باللغة المختارة، لذلك أظهرنا الدروس المتوفرة بلغات أخرى.";

        }

        else {

            indexStatus.textContent =
                "تم تحميل الدروس المفهرسة باللغة المختارة.";

        }

    }

}
