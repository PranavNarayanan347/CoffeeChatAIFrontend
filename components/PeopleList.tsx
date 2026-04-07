import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Mail, Linkedin, Building, GraduationCap } from "lucide-react";
import { Person } from "../services/api";

interface PeopleListProps {
  people: Person[];
  onGenerateEmail: (person: Person) => void;
}

export function PeopleList({ people, onGenerateEmail }: PeopleListProps) {
  return (
    <div className="space-y-4">
      <div className="text-center mb-6">
        <h3 className="text-lg font-semibold text-amber-900 mb-2">
          Found {people.length} people matching your criteria
        </h3>
        <p className="text-sm text-amber-700">
          Select someone to generate a personalized email
        </p>
      </div>
      
      <div className="grid gap-4">
        {people.map((person, index) => (
          <Card key={index} className="p-4 bg-gradient-to-br from-white to-amber-50 border-amber-200 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-lg">
                    <span className="text-white font-semibold text-sm">
                      {person.name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <h4 className="text-amber-900 font-semibold text-lg">{person.name}</h4>
                    <p className="text-sm text-amber-700 font-medium">
                      {person.title} at {person.company}
                    </p>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  {person.work_email !== 'N/A' && (
                    <div className="flex items-center gap-2 text-amber-800">
                      <Mail className="w-4 h-4" />
                      <span>{person.work_email}</span>
                    </div>
                  )}
                  
                  {person.linkedin !== 'N/A' && (
                    <div className="flex items-center gap-2 text-amber-800">
                      <Linkedin className="w-4 h-4" />
                      <a 
                        href={person.linkedin} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:text-amber-600 underline"
                      >
                        LinkedIn Profile
                      </a>
                    </div>
                  )}
                  
                  {person.education && person.education.length > 0 && (
                    <div className="flex items-start gap-2 text-amber-800">
                      <GraduationCap className="w-4 h-4 mt-0.5" />
                      <div>
                        {person.education.map((edu, eduIndex) => (
                          <div key={eduIndex} className="text-xs">
                            {edu.school_name} {edu.degrees.length > 0 && `- ${edu.degrees.join(', ')}`}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="ml-4">
                <Button
                  onClick={() => onGenerateEmail(person)}
                  className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg px-4 py-2"
                >
                  <Mail className="w-4 h-4 mr-2" />
                  Generate Email
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}




