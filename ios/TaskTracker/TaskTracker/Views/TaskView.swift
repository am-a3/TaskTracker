//
//  TaskView.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 21/08/2024.
//

import SwiftUI
import SwiftData

struct TaskView: View {
    @Environment(\.modelContext) var modelContext
    @Environment(\.presentationMode) var presentationMode
    @Bindable var task: TaskLocal
    @Query var projects: [ProjectLocal]
    
    var body: some View {
        VStack {
            HStack {
                Text("Done: ")
                Button(action: {
                    task.is_done.toggle()
                }, label: {
                    Label("",systemImage: task.is_done ? "checkmark.square.fill" : "square")
                        .labelStyle(.iconOnly)
                        .foregroundColor(task.is_done ? .blue : .blue)
                        .imageScale(.large)
                })
                .padding(.leading, 8)
                Spacer()
                Button("Delete"){
                    modelContext.delete(task)
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
                    task.name,
                    text: $task.name
                )
            }
            HStack {
                Text("Description: ")
                TextField(
                    task.task_description,
                    text: $task.task_description,
                    axis: .vertical
                )
                .lineLimit(4)
                Spacer()
            }
            HStack {
                Text("Projects:")
                Picker("Select Project", selection: $task.project) {
                    ForEach(projects) { value in
                        Text(value.name).tag(value as ProjectLocal?)
                    }
                }
                .pickerStyle(MenuPickerStyle())
                Spacer()
            }
            HStack {
                Text("Location:")
                //TODO: Drop down here
                Spacer()
            }
            HStack {
                Text("Tags:")
                Spacer()
            }
            Spacer()
        }
    }
}

struct TasksView: View {
    @Environment(\.modelContext) var modelContext
    @Query var tasks: [TaskLocal]
    var body: some View {
        VStack {
            HStack {
                Spacer()
                Button("Create New")
                {
                    let new_task = TaskLocal(name: "New task")
                    modelContext.insert(new_task)
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
            ForEach(tasks) { value in
                HStack {
                    NavigationLink(destination: TaskView(task: value)){
                        Text(value.name)
                    }
                    .padding(.leading, 8)
                    Spacer()
                    Button(action: {
                        value.is_done.toggle()
                    }, label: {
                        Label("",systemImage: value.is_done ? "checkmark.square.fill" : "square")
                            .labelStyle(.iconOnly)
                            .foregroundColor(value.is_done ? .blue : .blue)
                            .imageScale(.large)
                    })
                    .padding(.trailing, 8)
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}
