//
//  TaskTrackerApp.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 07/08/2024.
//

import SwiftUI
import SwiftData

@main
struct TaskTrackerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [TaskLocal.self, ProjectLocal.self])
    }
}
