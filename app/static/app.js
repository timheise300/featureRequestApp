function featureRequest(data) {
    this.id = ko.observable(data.id);
    this.title = ko.observable(data.title);
    this.description = ko.observable(data.description);
    this.clientName = ko.observable(data.clientName);
    this.priority = ko.observable(data.priority);
    this.targetDate = ko.observable(data.targetDate);
    this.productArea = ko.observable(data.productArea);
}

function client(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.featureRequests = ko.utils.arrayMap(data.featureRequests, function(item) {
        return new featureRequest(item);
    });
}

function featureRequestListVM() {
    var self = this;
    self.clients = ko.observableArray();
    self.productAreasList = ko.observableArray([]);
    self.newFeatureRequest = ko.observable(new featureRequest());
    self.selectedClient = ko.observable();

    // $.getJSON('/api/getAllClientData', function(clients) {
    //     var t = $.map(clients, function(item) {
    //         return new client(item);
    //     });
    //     self.clients(t);
    // });

    self.save = function() {
        return $.ajax({
            url: '/api/newRequest',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(self.NewFeatureRequest),
            success: function(data) {
                self.selectedClient.featureRequests.push(new featureRequest(self.newFeatureRequest));
                return;
            },
            error: function() {
            return console.log("Failed to add new Feature Request");
            }
        });
    };
}

ko.applyBindings(new featureRequestListVM());