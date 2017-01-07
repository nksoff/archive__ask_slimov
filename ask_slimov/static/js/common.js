var App = {};
(function ($) {
    // ajax csrf
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    App = {
        on_error: function (msg) {
            if (alertify == undefined) {
                return alert(msg);
            }
            return alertify.error(msg);
        },

        on_success: function (msg) {
            if (alertify == undefined) {
                return alert(msg);
            }
            return alertify.success(msg);
        },

        like_question: function (question_id, value) {
            $.ajax({
                'url': '/ajax/question/like/' + question_id,
                'type': 'POST',
                'data': {'value': value}
            }).success(function (data) {
                if (data.status == 'error') {
                    App.on_error(data.message);
                    return;
                }
                $('[data-question-like-count="' + data.question_id + '"]').text(data.likes);
            }).error(function () {
                App.on_error('Не удалось проголосовать за вопрос');
            });
        },

        like_answer: function (answer_id, value) {
            $.ajax({
                'url': '/ajax/answer/like/' + answer_id,
                'type': 'POST',
                'data': {'value': value}
            }).success(function (data) {
                if (data.status == 'error') {
                    App.on_error(data.message);
                    return;
                }
                $('[data-answer-like-count="' + data.answer_id + '"]').text(data.likes);
            }).error(function () {
                App.on_error('Не удалось проголосовать за ответ');
            });
        },

        correct_answer: function (answer_id) {
            $.ajax({
                'url': '/ajax/answer/correct/' + answer_id,
                'type': 'POST',
                'data': {}
            }).success(function (data) {
                if (data.status == 'error') {
                    App.on_error(data.message);
                    return;
                }
                $('[data-answer-correct]')
                    .removeClass('ask-answer-button-correct')
                    .addClass('ask-answer-button-incorrect');

                $('[data-answer-correct=' + data.answer_id + ']')
                    .removeClass('ask-answer-button-incorrect')
                    .addClass('ask-answer-button-correct');
            }).error(function () {
                App.on_error('Не удалось пометить ответ правильным');
            });
        },

        answers_loading: false,

        set_answers_loading: function (val) {
            val = !!val;
            this.answers_loading = val;

            $('.ask-answers-loading').toggle(val);
            $('.ask-answers-more').toggle(!val);
        },

        get_answers: function (question_id, page) {
            page = page || 1;

            if (this.answers_loading) return;
            this.set_answers_loading(true);

            $.ajax({
                'url': '/ajax/question/answers/' + question_id + '/' + page + '/',
                'type': 'GET'
            }).success(
                function (data) {
                    this.set_answers_loading(false);
                    if (data.status == 'error') {
                        App.on_error(data.message);
                        return;
                    }

                    $('.ask-answers-container').append(data.answers);
                    $('.ask-answers-more').data('page', parseInt(data.page) + 1);

                    if(data.limit_to >= data.total) {
                        $('.ask-answers-more').hide();
                    }
                }.bind(this)
            ).error(function () {
                App.on_error('Не удалось загрузить ответы');
            });
        },

        comet: function (channel) {
            var that = this;
            var self = function () {
                return that.comet(channel);
            };

            $.ajax({
                type: 'GET',
                url: '/comet-listen/' + channel
            }).success(function (data) {
                if (data != undefined && data.messages != undefined) {
                    for (var i in data.messages) {
                        that.on_success(data.messages[i]);
                    }
                }
                self();
            }).error(function () {
                setTimeout(self, 10000);
            });
        }
    };

    $(function () {
        $('[data-question-like-down]:not([disabled])').on('click', function () {
            // dislike question
            App.like_question($(this).data('question-like-down'), -1);
        });
        $('[data-question-like-up]:not([disabled])').on('click', function () {
            // like question
            App.like_question($(this).data('question-like-up'), 1);
        });
        $('.ask-answers-container').on('click', '[data-answer-like-down]:not([disabled])', function () {
            // dislike answer
            App.like_answer($(this).data('answer-like-down'), -1);
        }).on('click', '[data-answer-like-up]:not([disabled])', function () {
            // like answer
            App.like_answer($(this).data('answer-like-up'), 1);
        }).on('click', '[data-answer-correct]:not([disabled])', function () {
            // make answer correct
            App.correct_answer($(this).data('answer-correct'));
        });
    });
})(jQuery);
