(function (window, $) {
    var Gobang_Game = function () {
        var $board = $('.board table');
        this.init = function () {
            $board.children('tbody').html('');
            var trs = "";
            for (var i = 0; i < 15; i++) {
                trs += "<tr>";
                for (var j = 0; j < 15; j++) {
                    if (i == 6 && j == 6) {
                        trs += "<td class='chese white_chese'></td>>";
                    } else if (i == 8 && j == 8) {
                        trs += "<td class='chese black_chese'></td>>";
                    } else {
                        trs += "<td></td>>";
                    }
                }
                trs += '</td>';
            }
            $board.children('tbody').html(trs);
        }
        this.drawChese = function (type, pos) {
            var kalss = type == 'black' ? 'chese black_chese' : 'chese white_chese';
            $board.children('tbody').children('tr').eq(pos[0]).children('td').eq(pos[1]).addClass('played').append('<div class="' + kalss + '"></div>');
        }
        this.cheseEventListen = function () {
            var that = this;
            $board.children('tbody').click(function (e) {
                var chese = $(e.target);
                if (chese.closest('td').hasClass('played')) {
                    return;
                }
                var ver_index = chese.closest('tr').index(), hor_index = chese.index();
                that.drawChese('white', [ver_index, hor_index]);
                that.submit([ver_index, hor_index]);
            });
        }
        this.submit = function (pos) {
            var that = this;
            $.ajax({
                url: '/gobang/submit.do',
                dataType: 'JSON',
                method: 'GET',
                data: {
                    ver_index: pos[0],
                    hor_index: pos[1]
                },
                success: function (resp) {
                    if (resp.success) {
                        if (resp.ver_index && resp.hor_index) {
                            that.drawChese('black', [resp.ver_index, resp.hor_index])
                        }
                        if (resp.message) {
                            alert(resp.message)
                            window.location.reload();
                        }
                    }
                }
            });
        }
    }
    var gobang_game = new Gobang_Game();
    gobang_game.init();
    gobang_game.cheseEventListen();
})(window, jQuery);