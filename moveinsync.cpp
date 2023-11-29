#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

using namespace std;

class SystemMonitor {
public:
    static void logEvent(const string& event) {
        cout << "Event: " << event << endl;
    }
};

class Feedback;

class Trip {
public:
    Trip(const string& tripId, const string& driverName)
        : tripId(tripId), driverName(driverName) {}

    string getTripId() const {
        return tripId;
    }

    string getDriverName() const {
        return driverName;
    }

    void addFeedback(const Feedback& feedback);

    const vector<Feedback>& getFeedbacks() const {
        return feedbacks;
    }

private:
    string tripId;
    string driverName;
    vector<Feedback> feedbacks;
};

class Feedback {
public:
    Feedback(const string& travelerUsername, const string& driverName, const string& comments, const string& tripId)
        : travelerUsername(travelerUsername), driverName(driverName), comments(comments), tripId(tripId) {}

    string getTravelerUsername() const {
        return travelerUsername;
    }

    string getDriverName() const {
        return driverName;
    }

    string getComments() const {
        return comments;
    }

private:
    string travelerUsername;
    string driverName;
    string comments;
    string tripId;
};

class User {
public:
    User(const string& username, const string& password)
        : username(username), password(password) {}

    string getUsername() const {
        return username;
    }

    bool authenticate(const string& providedPassword) const {
        return password == providedPassword;
    }

private:
    string username;
    string password;
};

class Traveler : public User {
public:
    Traveler(const string& username, const string& password)
        : User(username, password) {}

    void submitFeedback(Trip& trip, const string& feedbackText);
};

class TransportManager : public User {
public:
    TransportManager(const string& username, const string& password)
        : User(username, password) {}

    void viewAllFeedback(const vector<Trip>& trips) const;
    void viewTripFeedback(const Trip& trip) const;
    void viewAggregatedFeedback(const vector<Trip>& trips) const;
    void evaluateDriverFeedback(const vector<Trip>& trips, const string& driverName) const;
};

class AuthenticationManager {
public:
    void addTraveler(const Traveler& traveler);
    void addTransportManager(const TransportManager& manager);
    bool authenticateUser(const string& username, const string& password);

    string generateUniqueTripId() const;

private:
    unordered_map<string, Traveler> travelers;
    unordered_map<string, TransportManager> transportManagers;
};

void Trip::addFeedback(const Feedback& feedback) {
    feedbacks.push_back(feedback);
}

void Traveler::submitFeedback(Trip& trip, const string& feedbackText) {
    string feedbackId = trip.getDriverName() + "_" + getUsername();
    Feedback feedback(getUsername(), trip.getDriverName(), feedbackText, trip.getTripId());
    trip.addFeedback(feedback);
    SystemMonitor::logEvent("Feedback submitted by " + getUsername() + " for trip " + trip.getTripId());
}

void TransportManager::viewAllFeedback(const vector<Trip>& trips) const {
    cout << "Viewing all feedback:\n";
    for (const auto& trip : trips) {
        for (const auto& feedback : trip.getFeedbacks()) {
            cout << "Trip ID: " << trip.getTripId() << ", Feedback: " << feedback.getComments() << "\n";
        }
    }
}

void TransportManager::viewTripFeedback(const Trip& trip) const {
    cout << "Viewing feedback for trip " << trip.getTripId() << ":\n";
    for (const auto& feedback : trip.getFeedbacks()) {
        cout << "Feedback: " << feedback.getComments() << "\n";
    }
}

void TransportManager::viewAggregatedFeedback(const vector<Trip>& trips) const {
    cout << "Viewing aggregated feedback for all trips:\n";
    for (const auto& trip : trips) {
        for (const auto& feedback : trip.getFeedbacks()) {
            cout << "Driver: " << feedback.getDriverName() << ", Feedback: " << feedback.getComments() << "\n";
        }
    }
}

void TransportManager::evaluateDriverFeedback(const vector<Trip>& trips, const string& driverName) const {
    cout << "Evaluating feedback for driver " << driverName << ":\n";
    for (const auto& trip : trips) {
        if (trip.getDriverName() == driverName) {
            for (const auto& feedback : trip.getFeedbacks()) {
                cout << "Trip ID: " << trip.getTripId() << ", Feedback: " << feedback.getComments() << "\n";
            }
        }
    }
}

void AuthenticationManager::addTraveler(const Traveler& traveler) {
    travelers.emplace(traveler.getUsername(), traveler);
}

void AuthenticationManager::addTransportManager(const TransportManager& manager) {
    transportManagers.emplace(manager.getUsername(), manager);
}

bool AuthenticationManager::authenticateUser(const string& username, const string& password) {
    auto travelerIt = travelers.find(username);
    if (travelerIt != travelers.end()) {
        return travelerIt->second.authenticate(password);
    }

    auto managerIt = transportManagers.find(username);
    if (managerIt != transportManagers.end()) {
        return managerIt->second.authenticate(password);
    }

    return false;
}

string AuthenticationManager::generateUniqueTripId() const {
    static int tripCounter = 0;
    return "T" + to_string(tripCounter++);
}

int main() {
    AuthenticationManager authManager;

    // Add Traveler and TransportManager to the system
    Traveler traveler("john_traveler", "travel123");
    TransportManager transportManager("admin_transport", "adminPass");

    authManager.addTraveler(traveler);
    authManager.addTransportManager(transportManager);
    // Authenticate users
    if (authManager.authenticateUser("john_traveler", "travel123")) {
        cout << "Traveler authenticated successfully.\n";
    } else {
        cout << "Traveler authentication failed.\n";
    }

    if (authManager.authenticateUser("admin_transport", "adminPass")) {
        cout << "Transport Manager authenticated successfully.\n";
    } else {
        cout << "Transport Manager authentication failed.\n";
    }

    // Create a sample trip
    string tripId = authManager.generateUniqueTripId();
    Trip trip(tripId, "SampleDriver");

    // Traveler submits feedback
    traveler.submitFeedback(trip, "Great trip, awesome driver!");

    // Transport Manager reviews feedback
    vector<Trip> trips{trip};
    transportManager.viewAllFeedback(trips);
    transportManager.viewTripFeedback(trip);
    transportManager.viewAggregatedFeedback(trips);
    transportManager.evaluateDriverFeedback(trips, "SampleDriver"); 

    return 0;
}
