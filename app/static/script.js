$(".addDiceButton").click(function(){
    dice_type = $(this).attr("id")
    dice_id = Math.floor(Math.random()*16777215).toString(16)
    $.ajax({
        type: "POST",
        url: "/api/v1/add_dice",
        contentType: 'application/json',
        data: JSON.stringify({dice_id: dice_id, dice_type: dice_type}),
        success: refreshDice,
    });
});

$("#rollButton").click(function(){
    $.ajax({
        type: "POST",
        url: "/api/v1/roll",
        success: refreshDice
    });
});

function refreshDice() {
    $.get("/api/v1/get_dice").done(function(data){
        $(".canvas").empty();
        for (let dice_id in data) {
            dice_type = data[dice_id]["d"]
            value = data[dice_id]["value"] | "?"

            // Create dice element
            let container = $('<div class="dice_container"></div>');
            let dice = $('<div class="dice"></div>');
            let roll = $('<label class="roll">' + value + '</label>');
            let type = $('<label class="type">' + dice_type + '</label>');
            let color = "#" + dice_id;
            dice.css("background-color", color);
            container.append(dice.append(roll)).append(type);

            dice.on("click", function(){
                $.ajax({
                    type: "POST",
                    url: "/api/v1/remove_dice",
                    contentType: 'application/json',
                    data: JSON.stringify({dice_id: dice_id}),
                    success: function() { container.fadeOut() }
                });
            });

            // Append it to canvas
            $(".canvas").append(container);
        }
    })
}






