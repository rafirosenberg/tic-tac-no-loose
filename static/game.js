function MakeMove(sender, move) {
    if ($(sender).text().trim() == "") {
        $(sender).html(player);

        $.post(create_url, {'move': move},
            function(data) {
                // successfully made a move
            }
        )
    }
}