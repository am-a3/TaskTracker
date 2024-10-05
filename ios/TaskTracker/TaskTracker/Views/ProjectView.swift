//
//  ProjectView.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 21/08/2024.
//

import SwiftUI
import SwiftData

struct ProjectView: View {
    @Environment(\.modelContext) var modelContext
    @Environment(\.presentationMode) var presentationMode
    @Bindable var project: ProjectLocal
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                Button("Delete"){
                    modelContext.delete(project)
                    presentationMode.wrappedValue.dismiss()
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
                .frame(height: 2)
                .background(Color.blue)
            HStack{
                Text("Name: ")
                TextField(
                    project.name,
                    text: $project.name
                )
            }
            HStack {
                Text("Description: ")
                TextField(
                    project.project_description,
                    text: $project.project_description,
                    axis: .vertical
                )
                .lineLimit(4)
                Spacer()
            }
            HStack {
                Text("Tasks:")
                List {
                    ForEach(project.tasks) { task in
                        Text(task.name)
                    }
                }
                Spacer()
            }
            Spacer()
        }
    }
}

struct ProjectsView: View {
    @Environment(\.modelContext) var modelContext
    @Query var projects: [ProjectLocal]
    var body: some View {
        VStack {
            HStack {
                Spacer()
                Button("Create New")
                {
                    let new_project = ProjectLocal(name: "New project")
                    modelContext.insert(new_project)
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            ForEach(projects) { value in
                HStack {
                    NavigationLink(destination: ProjectView(project: value)){
                        Text(value.name)
                    }
                    .padding(.leading, 8)
                    Spacer()
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}
