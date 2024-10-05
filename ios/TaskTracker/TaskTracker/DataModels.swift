//
//  DataModels.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 17/08/2024.
//

import Foundation

struct TaskBasic: Codable, Hashable {
    var id: String = ""
    var name: String = ""
    var is_done: Bool = false
}

struct Task: Codable, Hashable {
    var id: String = ""
    var name: String = ""
    var description: String = ""
    var project_name: String = ""
    var location_name: [String] = []
    var is_done: Bool = false
    var tags: [String] = []
}

struct ProjectBasic: Codable, Hashable {
    var id: String = ""
    var name: String = ""
}

struct Project: Codable, Hashable {
    var id: String = ""
    var name: String = ""
    var description: String = ""
}

struct LocationBasic: Codable, Hashable {
    var id: String
    var name: String
}

struct Location: Codable, Hashable {
    var id: String
    var name: String
    var description: String
}

struct TagBasic: Codable, Hashable {
    var id: String
    var name: String
}

struct Tag: Codable, Hashable {
    var id: String
    var name: String
    var description: String
}
