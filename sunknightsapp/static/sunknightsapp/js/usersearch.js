
$(document).ready(function () {

  $('#usersearch').selectize({
    valueField: 'discord_id',
    labelField: 'discord_nickname',
    searchField: 'discord_nickname',
    maxItems: 1,
    create: false,
    onItemAdd: function (item) {
       console.log(item)
      window.location.href = "/user/"+item;
    },
    render: {
      option: function(item, escape) {
        var avatarurl=""
        if (item.avatar==""){
          avatarurl="https://discordapp.com/assets/322c936a8c8be1b803cd94861bdfa868.png"
        }else{
          avatarurl="https://cdn.discordapp.com/avatars/"+item.discord_id+"/"+item.avatar
        }

        var avatar="<img class='leaderpoint-avatar img-circle' src='"+avatarurl+"'>"


        return '<div>' +
          '<span class="title"><span class="name">'+avatar+escape(item.discord_nickname)+'</span></span>'+
          '</div>';
      }
    },
    score: function(search) {

      var score = this.getScoreFunction(search);
      return function(item) {
        return score(item)*item.id;
      };
    },
    load: function(query, callback) {
      if (!query.length) return callback();

      $.ajax({
        url     : ajaxhandlerurl,

          type    : 'POST',
          dataType: 'json',
          headers: {
          'X-CSRFToken': $.cookie('csrftoken')
        },
        // Use "{{{q}}}" as a placeholder and Ajax Bootstrap Select will
        // automatically replace it with the value of the search query.
        data    : {
          searchusers: query,
            ajax_action_id:ajaxactions.RETRIEVEUSERSTOFIGHTAGAINST
        },
        error: function() {
          callback();
        },
        success: function(res) {
          callback(res.message.data);
        }
      })



    }
  });



});