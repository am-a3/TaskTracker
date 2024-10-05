//
//  ContentView.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 07/08/2024.
//

import SwiftUI
import SwiftData

struct ContentView: View {
    @ObservedObject private var viewModel = ViewModel()
    
    var body: some View {
        NavigationView {
            VStack {
                Spacer()
                NavigationLink(destination: TasksView()){
                    Text("TASKS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.bottom, 20)
                NavigationLink(destination: ProjectsView()){
                    Text("PROJECTS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.bottom, 20)
                NavigationLink(destination: LocationsView()){
                    Text("LOCATIONS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.bottom, 20)
                NavigationLink(destination: TagsView()){
                    Text("TAGS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                Spacer()
            }
            .padding()
        }
    }
}

#Preview {
    ContentView()
        .modelContainer(for: [TaskLocal.self, ProjectLocal.self], inMemory: true)
}
